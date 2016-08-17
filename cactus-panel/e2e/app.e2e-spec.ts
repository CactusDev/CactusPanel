import { CactusPanelPage } from "./app.po";

describe("cactus-panel App", function() {
  let page: CactusPanelPage;

  beforeEach(() => {
    page = new CactusPanelPage();
  });

  it("should display message saying app works", () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual("app works!");
  });
});
