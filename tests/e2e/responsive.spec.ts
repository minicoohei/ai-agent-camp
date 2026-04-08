import { test, expect } from '@playwright/test';

const viewports = [
  { name: 'mobile', width: 375, height: 667 },
  { name: 'tablet', width: 768, height: 1024 },
  { name: 'desktop', width: 1280, height: 800 },
];

test.describe('Responsive Design', () => {
  for (const viewport of viewports) {
    test(`home page renders correctly at ${viewport.name}`, async ({ page }) => {
      await page.setViewportSize({ width: viewport.width, height: viewport.height });
      await page.goto('/index.html');

      // Check hero section is visible
      const hero = page.locator('.hero-gradient, .hero');
      await expect(hero.first()).toBeVisible();

      // Check navigation is accessible
      if (viewport.width >= 992) {
        await expect(page.locator('.navbar-nav')).toBeVisible();
      }

      // Take screenshot for visual reference
      await page.screenshot({
        path: `tests/e2e/screenshots/home-${viewport.name}.png`,
        fullPage: true,
      });
    });

    test(`module-1 renders correctly at ${viewport.name}`, async ({ page }) => {
      await page.setViewportSize({ width: viewport.width, height: viewport.height });
      await page.goto('/modules/1-banner/index.html');

      // Check main content is visible
      await expect(page.locator('.hero')).toBeVisible();
      await expect(page.locator('.section').first()).toBeVisible();

      // Take screenshot
      await page.screenshot({
        path: `tests/e2e/screenshots/module-1-${viewport.name}.png`,
        fullPage: true,
      });
    });
  }
});

test.describe('Mobile Navigation', () => {
  test('hamburger menu works on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/index.html');

    // Check if toggler exists
    const toggler = page.locator('.navbar-toggler');
    if (await toggler.isVisible()) {
      await toggler.click();
      // Wait for collapse animation
      await page.waitForTimeout(500);
      // Check menu is expanded
      await expect(page.locator('.navbar-collapse.show, .navbar-collapse.collapsing')).toBeVisible();
    }
  });
});
