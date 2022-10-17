const fs = require('fs');
const finnhub = require('finnhub');
const myApiKey = require('./my-api-key');
const symbols = require('./symbols');

// eslint-disable-next-line camelcase
const { api_key } = finnhub.ApiClient.instance.authentications;

// eslint-disable-next-line camelcase
api_key.apiKey = myApiKey;

const finnhubClient = new finnhub.DefaultApi();

// const now = Math.floor(Number(Date.now()) / 1000);

// console.log(now);

const from = 1634432000;
const to = 1665882000;

const erroredSymbols = [];
const dataArray = [];

// we'll mutate the symbols array as we go

let symbol = symbols.pop();
const getNextSymbol = function getNextSymbol() {
  finnhubClient.stockCandles(symbol, 'D', from, to, (error, {
    o: open, h: high, l: low, c: close, v: volume, t: timestamp,
  }) => {
    if (error) {
      erroredSymbols.push(symbol);
    } else {
      for (let i = 0; i < open.length; i += 1) {
        const date = new Date(timestamp[i] * 1000).toLocaleDateString();
        const dataEntry = dataArray.find((entry) => entry.date === date);
        if (dataEntry) {
          dataEntry[symbol] = {
            open: open[i], high: high[i], low: low[i], close: close[i], volume: volume[i],
          };
        } else {
          dataArray.push({
            date,
            [symbol]: {
              open: open[i], high: high[i], low: low[i], close: close[i], volume: volume[i],
            },
          });
        }
      }
    }

    symbol = symbols.pop();
    if (symbol) {
      setTimeout(getNextSymbol, 1000);
      console.log(symbol);
      console.log(symbols.length);
    } else {
      fs.writeFileSync('./retrieved-data.json', JSON.stringify(dataArray));
      fs.writeFileSync('./errored-symbols.json', JSON.stringify(erroredSymbols));
    }
  });
};

getNextSymbol();
