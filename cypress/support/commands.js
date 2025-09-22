// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
Cypress.Commands.add('login', (username, password) => {
  cy.visit('/login')  
  cy.get('input[name=userName]').type(username)
  // {enter} causes the form to submit
  cy.get('input[name=password]').type(`${password}{enter}`, { log: false })
})