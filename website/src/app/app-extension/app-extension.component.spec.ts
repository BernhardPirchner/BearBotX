import { TestBed } from '@angular/core/testing';
import { AppExtensionComponent } from './app-extension.component';
 
describe('AppComponent', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AppExtensionComponent],
    }).compileComponents();
  });
 
  it('should create the app', () => {
    const fixture = TestBed.createComponent(AppExtensionComponent);
    const app = fixture.componentInstance;
    expect(app).toBeTruthy();
  });
 
  /*it(`should have the 'website' title`, () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;
    expect(app.title).toEqual('website');
  });*/
 
  it('should render title', () => {
    const fixture = TestBed.createComponent(AppExtensionComponent);
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('h1')?.textContent).toContain('Hello, website');
  });
});