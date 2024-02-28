import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LandingComponent } from './components/landing/landing.component';
import { AnalyticsComponent } from './components/analytics/analytics.component';
import { MinifiersComponent } from './components/minifiers/minifiers.component';
import { GeneratorsComponent } from './components/generators/generators.component';

const routes: Routes = [
  { path: '', component: LandingComponent },
  { path: 'analytics', component: AnalyticsComponent },
  { path: 'minifiers', component: MinifiersComponent },
  { path: 'generators', component: GeneratorsComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
