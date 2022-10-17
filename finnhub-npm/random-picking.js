const retrievedData = require('./retrieved-data.json');

const randomlyPick = () => (
  retrievedData.reduce((acc, e, i) => (
    Object.keys(e).filter((key) => !key.includes('/')).reduce((max, key) => (
      (e[key].high / e[key].open)
    ), -Infinity)
  ), 1000)
);
