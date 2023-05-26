document.addEventListener("DOMContentLoaded", () => {
  const scrapeButton = document.getElementById("scrapeButton");

  scrapeButton.addEventListener("click", async () => {
    try {
      const data = await scrapeGoogleMaps();
      displayData(data);
    } catch (error) {
      console.error("Failed to scrape data:", error);
    }
  });
});

async function scrapeGoogleMaps() {
  // Existing code for scraping Google Maps
  const playwright = require('playwright');

  const search_for = process.argv[2] || 'Ahmedabad,school';
  const total = parseInt(process.argv[3]) || 3;
  
  async function scrapeGoogleMaps() {
    const l1 = [];
    const l2 = [];
    const l3 = [];
    const l4 = [];
    const l5 = [];
  
    const browser = await playwright.chromium.launch({ headless: true });
    const context = await browser.newContext();
    const page = await context.newPage();
  
    await page.goto('https://www.google.com/maps', { timeout: 60000 });
    await page.waitForTimeout(5000);
  
    const searchInput = await page.$('//input[@id="searchboxinput"]');
    await searchInput.fill(search_for);
    await page.waitForTimeout(3000);
  
    await page.keyboard.press('Enter');
    await page.waitForTimeout(5000);
  
    let l = 0;
    while (l < total) {
      await page.hover('(//div[@role="article"])[last()]');
      await page.waitForTimeout(3000);
  
      const listings = await page.$$('//div[@role="article"]');
      for (const listing of listings.slice(0, total)) {
        await listing.click();
        await page.waitForTimeout(5000);
  
        const nameXPath = '//h1[contains(@class,"fontHeadlineLarge")]';
        const addressXPath = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]';
        const websiteXPath = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]';
        const phoneNumberXPath = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]';
        const reviewsSpanXPath = '//span[@role="img"]';
  
        const nameCount = await page.$eval(nameXPath, (el) => el.innerText ? 1 : 0);
        const addressCount = await page.$eval(addressXPath, (el) => el.innerText ? 1 : 0);
        const websiteCount = await page.$eval(websiteXPath, (el) => el.innerText ? 1 : 0);
        const phoneNumberCount = await page.$eval(phoneNumberXPath, (el) => el.innerText ? 1 : 0);
        const reviewsSpanCount = await listing.$eval(reviewsSpanXPath, (el) => el.getAttribute('aria-label') ? 1 : 0);
  
        const name = nameCount > 0 ? await page.$eval(nameXPath, (el) => el.innerText) : '';
        const address = addressCount > 0 ? await page.$eval(addressXPath, (el) => el.innerText) : '';
        const website = websiteCount > 0 ? await page.$eval(websiteXPath, (el) => el.innerText) : '';
        const phoneNumber = phoneNumberCount > 0 ? await page.$eval(phoneNumberXPath, (el) => el.innerText) : '';
        const reviews = reviewsSpanCount > 0 ? parseInt(await listing.$eval(reviewsSpanXPath, (el) => el.getAttribute('aria-label').split(' ')[2].replace(',', ''))) : '';
  
        l1.push(name);
        l2.push(address);
        l3.push(website);
        l4.push(phoneNumber);
        l5.push(reviews);
  
        l++;
        if (l >= total) {
          break;
        }
      }
    }
  
    const data = {
      'name': l1,
      'address':l2,
      'website' :l3,
      'phoneNumber':l4,
      'reviews': l5
    }}

    return data;
}

function displayData(data) {
  const dataContainer = document.getElementById("dataContainer");
  dataContainer.innerHTML = "";

  for (const item of data) {
    const itemElement = document.createElement("ul");
    itemElement.textContent = item;

    dataContainer.appendChild(itemElement);
  }
}
