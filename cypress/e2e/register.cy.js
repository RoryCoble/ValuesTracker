function register(username, password, email) {
  cy.get('[data-testid="usernameInput"]').type(username)
  cy.get('[data-testid="passwordInput"]').type(password)
  cy.get('[data-testid="emailInput"]').type(email)
  cy.get('[data-testid="submitButton"]').click()
}

describe('Register page', () => {

  beforeEach(() => {
    let query = 'TRUNCATE TABLE public.users, public.user_entities;'
    const host = Cypress.env('database')
    const port = Cypress.env('database_port')
    let user = 'api'    
    cy.task('databaseQuery', { query, host, port, user })
    cy.visit('/')
    cy.get('[data-testid="registerLink"]').dblclick()
  })    
    
  it('displays the expected elements', () => {
    cy.get('[data-testid="pageTitle"]').should('be.visible').and('have.text', 'Register')
    cy.get('[data-testid="usernameInput"]').should('be.visible').and('have.attr', 'placeholder', 'User Name')
    cy.get('[data-testid="passwordInput"]').should('be.visible').and('have.attr', 'placeholder', 'Password')  
    cy.get('[data-testid="emailInput"]').should('be.visible').and('have.attr', 'placeholder', 'Email')
    cy.get('[data-testid="submitButton"]').should('be.visible').and('have.text', 'Submit')
    cy.get('[data-testid="cancelLink"]').should('be.visible').and('have.text', 'Cancel')
  })

  it('returns to the login page when cancel is clicked', () => {
    cy.get('[data-testid="cancelLink"]').dblclick()
    cy.url().should('include', '/login')  
  })

  it('sucessfully registers a new user', () => {
    register('a','a','a')
    cy.url().should('include', '/login')    
  })

  it('throws an error when someone tries to register an existing user', () => {
    register('a','a','a')
    cy.contains('Register').dblclick()
    register('a','a','a')
    cy.get('li[data-sonner-toast]').should('be.visible').and('have.text', 'User failed to be created')
  })
})