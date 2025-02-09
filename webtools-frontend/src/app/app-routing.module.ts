import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LandingComponent } from './components/landing/landing.component';
import { MinifiersComponent } from './components/minifiers/minifiers.component';
import { GeneratorsComponent } from './components/generators/generators.component';
import { PageinsightsComponent } from './components/pageinsights/pageinsights.component';
import { DomaincheckComponent } from './components/domaincheck/domaincheck.component';
import { RepoanalyzerComponent } from './components/repoanalyzer/repoanalyzer.component';

const routes: Routes = [
  { path: '', component: LandingComponent },
  { path: 'domain-check', component: DomaincheckComponent },
  { path: 'minifiers', component: MinifiersComponent },
  { path: 'generators', component: GeneratorsComponent },
  { path: 'page-insights', component: PageinsightsComponent },
  { path: 'repo-analyzer', component: RepoanalyzerComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule { }
