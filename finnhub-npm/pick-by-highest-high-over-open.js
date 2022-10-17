const retrievedData = require('./retrieved-data.json');



const pickByHighestHighOverOpen = () => (
  retrievedData.reduce((acc, e, i) => {
    Object.keys(e).filter((key) => !key.includes('/')).find((findKey) =>.reduce((max, key) => (
      (e[key].high / e[key].open)
    ), -Infinity))
  }, 1000)
);
