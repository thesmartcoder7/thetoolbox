import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LandingComponent } from './components/landing/landing.component';
import { AnalyticsComponent } from './components/analytics/analytics.component';
import { MinifiersComponent } from './components/minifiers/minifiers.component';
import { GeneratorsComponent } from './components/generators/generators.component';
import { PageinsightsComponent } from './components/pageinsights/pageinsights.component';

const routes: Routes = [
  { path: '', component: LandingComponent },
  { path: 'analytics', component: AnalyticsComponent },
  { path: 'minifiers', component: MinifiersComponent },
  { path: 'generators', component: GeneratorsComponent },
  { path: 'page-insights', component: PageinsightsComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
