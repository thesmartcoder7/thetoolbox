import { environment as devEnv } from './environment.development';
import { environment as prodEnv } from './environment.production';

let production = false; // Set this to true for production build

export const environment = {
  apiUrl: production ? prodEnv.apiUrl : devEnv.apiUrl,
  sampleRepo: production ? prodEnv.sampleRepo : devEnv.sampleRepo,
};
