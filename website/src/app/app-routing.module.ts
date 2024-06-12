import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { AppExtensionComponent } from './app-extension/app-extension.component';

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'app-extension', component: AppExtensionComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }