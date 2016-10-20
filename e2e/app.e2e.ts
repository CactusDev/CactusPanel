import { CactusPanelPage } from './app.po';

describe('cactuspanel App', function() {
  let page: CactusPanelPage;

  beforeEach(() => {
    page = new CactusPanelPage();
  })

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('cactuspanel works!');
  });
});
