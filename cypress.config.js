const { defineConfig } = require("cypress");
const { Client } = require('pg')

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    setupNodeEvents(on, config) {
      on('task', {
        userDb: async (query) => {
          const client = new Client({
            user: 'api',
            password: 'data',
            host: 'localhost',
            database: 'EntitiesAndValues',
            port: 5431
          })
          await client.connect()
          const res = await client.query(query)
          await client.end()
          return res.rows;
        },

        dataseederDb: async (query) => {
          const client = new Client({
            user: 'data_seeder',
            password: 'data',
            host: 'localhost',
            database: 'EntitiesAndValues',
            port: 5431
          })
          await client.connect()
          const res = await client.query(query)
          await client.end()
          return res.rows;
        },
      });
    },
  },
});
