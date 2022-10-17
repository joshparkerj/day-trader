const fs = require('fs');
const retrievedData = require('./retrieved-data.json');

const sorter = (date) => {
  const { month, day, year } = date.match(/^(?<month>\d+)\/(?<day>\d+)\/(?<year>\d+)$/).groups;

  return `${year}${month.padStart(2, '0')}${day.padStart(2, '0')}`;
};

fs.writeFileSync('./retrieved-data.json', JSON.stringify(retrievedData.sort((a, b) => (sorter(a.date) > sorter(b.date) ? 1 : -1))));
