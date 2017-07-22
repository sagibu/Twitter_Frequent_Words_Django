import { StaticPage } from './app.po';

describe('static App', () => {
  let page: StaticPage;

  beforeEach(() => {
    page = new StaticPage();
  });

  it('should display welcome message', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('Welcome to app!');
  });
});
