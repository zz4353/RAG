import asyncio
from playwright.async_api import async_playwright
import re

from database.postgresql import PhoneDB

class CellphoneSCrawler:
    def __init__(self,
                 base_url: str = "https://cellphones.com.vn/mobile.html",
                 database: PhoneDB = None,
                 headless: bool = True
                 ):
        self.base_url = base_url
        self.database = database
        self.headless = headless

    async def run(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            page = await browser.new_page()
            await page.goto(self.base_url, wait_until="domcontentloaded")
            await self._load_more(page)
            links = await self._get_link(page)

            for link in links:
                await self._get_item_infos(browser, link)
                
            # link = links[0]
            # await self._get_item_infos(browser, link)
            await browser.close()

    async def _get_link(self, page):
        await page.wait_for_selector(".product-list-filter .product-info-container.product-item")
        items = await page.query_selector_all(".product-list-filter .product-info-container.product-item")
        links = []
        for item in items:
            product_infos = await item.query_selector(".product-info")
            link = await product_infos.query_selector("a")
            new_product = await self._check_new_product(link)
            if not new_product:
                link = await link.get_attribute("href")
                links.append(link)
        # print(links)
        await page.close()
        return links

    async def _get_item_infos(self, browser, link):
        page = await browser.new_page()
        await page.goto(link, wait_until="domcontentloaded")
        versions = await self._get_all_versions(page)
        await page.close()
        infos = {}
        if not versions:
            versions = [link]
        for version in versions:
            page = await browser.new_page()
            await page.goto(version, wait_until="domcontentloaded")
            
            infos["url"] = version

            infos["title"] = await page.query_selector(".box-product-name")
            infos["title"] = await infos["title"].inner_text()

            infos["price"] = await page.query_selector(".smember-price-label .sale-price")
            infos["price"] = await infos["price"].inner_text()

            infos["colors"] = await self._get_all_colors(page)

            infos["specs"] = await self._get_specs(page)
            
            infos["images"] = await self._get_images(page)

            infos["description"] = await self._get_description(page)
            self.database.insert(infos)
            print(f"Inserted: {infos['title']}")
            await page.close()

    async def _get_all_versions(self, page):
        await page.wait_for_selector(".box-detail-product__box-center.column")
        try:
            list_version = await page.query_selector(".box-detail-product__box-center.column .box-linked .list-linked")

            versions = []
            version_links = await list_version.query_selector_all("a")
            for version_link in version_links:
                version_link = await version_link.get_attribute("href")
                version_link = f"https://cellphones.com.vn{version_link}"
                versions.append(version_link)
            # print(versions)
            return versions
        except Exception as e:
            print(f"No other versions")
            return []

    async def _get_all_colors(self, page):
        await page.wait_for_selector(".box-detail-product__box-center.column")
        try:
            list_color = await page.query_selector(".box-detail-product__box-center.column .box-product-variants .list-variants")

            colors = []
            color_titles = await list_color.query_selector_all("li")
            for color_title in color_titles:
                color_title = await color_title.query_selector("a")
                color_title = await color_title.get_attribute("title")
                colors.append(color_title)
            # print(colors)
            return colors
        except Exception as e:
            print(f"No other colors")
            return []

    async def _get_specs(self, page):
        specs = {}
        table_content = await page.query_selector("#thong-so-ky-thuat.cps-block-technicalInfo")
        table_content = await table_content.query_selector("table")
        rows = await table_content.query_selector_all("tr")
        for row in rows:
            cols = await row.query_selector_all("td")
            if len(cols) == 2:
                key = await cols[0].inner_text()
                value = await cols[1].inner_text()
                specs[key] = value
        return specs
    
    async def _get_images(self, page, image_size=200):
        images = await page.query_selector(".swiper-wrapper")
        image_elements = await images.query_selector_all("img")
        image_urls = []
        for img in image_elements:
            url = await img.get_attribute("src")
            if url:
                rsfill = f"rs:fill:{image_size}"
                url = re.sub(r"rs:fill:[^/]+", rsfill, url)
                image_urls.append(url)
        return image_urls
    
    async def _get_description(self, page):
        cps_content = await page.query_selector("#cpsContent.cps-block-content")

        return await cps_content.inner_text()

    async def _check_new_product(self, query_selector):
        check = False
        new_product_tag = await query_selector.query_selector(".product__more-info__item.notification.is-light.new-arrival")
        if new_product_tag:
            check = True
        return check

    async def _load_more(self, page, delay=2000):
        while True:
            try:
                load_more = await page.query_selector(".button__show-more-product")
                if load_more:
                    await load_more.click()
                    await page.wait_for_timeout(delay)
                else:
                    break
            except Exception as e:
                try:
                    await self._handle_popup(page)
                    print("handled")
                except Exception as e:
                    continue

    async def _handle_popup(self, page):
        ad_popup = await page.query_selector(".modal.popup-banner.is-active")
        if ad_popup:
            close_button = await ad_popup.query_selector("button")
            await close_button.click()
        subscribe_popup = await page.query_selector(".subscriber-popup.box-banner")
        if subscribe_popup:
            close_button = await subscribe_popup.query_selector("button.cancel-button-top")
            await close_button.click()


async def main():
    crawler = CellphoneSCrawler()
    await crawler.run()

if __name__ == "__main__":
    asyncio.run(main())