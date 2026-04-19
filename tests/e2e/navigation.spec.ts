import { test, expect } from '@playwright/test';

test.describe('Course Navigation', () => {
  test('home page loads correctly', async ({ page }) => {
    await page.goto('/index.html');
    await expect(page).toHaveTitle(/AIエージェント研修/);
    await expect(page.locator('h1')).toContainText('AIエージェント研修');
  });

  test('navigation to Foundation section', async ({ page }) => {
    await page.goto('/index.html');
    await page.click('a[href="#foundation"]');
    await expect(page.locator('#foundation')).toBeVisible();
  });

  test('navigation to Setup section', async ({ page }) => {
    await page.goto('/index.html');
    await page.click('a[href="#setup"]');
    await expect(page.locator('#setup')).toBeVisible();
  });

  test('navigation to Modules section', async ({ page }) => {
    await page.goto('/index.html');
    await page.click('a[href="#modules"]');
    await expect(page.locator('#modules')).toBeVisible();
  });

  test('module 1 link works', async ({ page }) => {
    await page.goto('/index.html');
    await page.click('a[href="modules/1-banner/index.html"]');
    await expect(page).toHaveURL(/1-banner/);
    await expect(page.locator('h1')).toContainText('バナー');
  });

  test('module 0 setup link works', async ({ page }) => {
    await page.goto('/index.html');
    await page.click('a[href="setup/module-0.html"]');
    await expect(page).toHaveURL(/module-0/);
    await expect(page.locator('h1')).toContainText('環境セットアップ');
  });
});

test.describe('Module Pages Format Consistency', () => {
  const modulePages = [
    '/modules/1-banner/index.html',
    '/modules/2-diagram/index.html',
    '/modules/3-screenshot/index.html',
    '/modules/4-data/index.html',
    '/modules/5-pptx/index.html',
    '/modules/6-search/index.html',
    '/modules/7-video/index.html',
    '/modules/8-gas/index.html',
    '/modules/9-actions/index.html',
    '/modules/10-notion/index.html',
    '/modules/11-agent/index.html',
  ];

  for (const pagePath of modulePages) {
    test(`${pagePath} has consistent format`, async ({ page }) => {
      await page.goto(pagePath);

      // Check hero section exists
      await expect(page.locator('.hero')).toBeVisible();

      // Check section-title exists
      await expect(page.locator('.section-title').first()).toBeVisible();

      // Check footer exists
      await expect(page.locator('.footer')).toBeVisible();
    });
  }
});
