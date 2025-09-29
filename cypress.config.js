const { defineConfig } = require("cypress");
const { Client } = require('pg')

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    env: {
        api: 'http://localhost:5001',
        dataseeder_api: 'http://localhost:5002',
        database: 'localhost',
        database_port: 5431,
    },
    setupNodeEvents(on, config) {
      on('task', {
        databaseQuery: async ({ query, host, port, user }) => {
          const client = new Client({
            user: user,
            password: 'data',
            host: host,
            database: 'EntitiesAndValues',
            port: port
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
