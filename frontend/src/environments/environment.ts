let liveTest = true; // Set this to true for production build
let apiUrl: string;

if (liveTest) {
  apiUrl = 'https://api.thetoolbox.website';
} else {
  apiUrl = 'http://localhost:8000';
}

export const environment = {
  apiUrl: apiUrl,
  sampleRepo: 'https://github.com/thesmartcoder7/thetoolbox',
};
