describe('Page Menu', () => {

  before(() => {
    let query = 'TRUNCATE TABLE public.users, public.user_entities;'
    const host = Cypress.env('database')
    const port = Cypress.env('database_port')
    let user = 'api'    
    cy.task('databaseQuery', { query, host, port, user })
    cy.request({
        method: 'POST', 
        url: Cypress.env('api') + '/api/create_user',
        form: true,
        body: { 
          userName : 'a', 
          password : 'a', 
          email : 'a' 
        },
    })
  })
    
  beforeEach(() => {
    cy.login('a','a')
    cy.get('[data-testid="menuButton"]').click()  
  })

  it('displays the expected links', () => {
    cy.get('[data-testid="homeButton"]').should('be.disabled').should('be.visible').and('have.text', 'Home')
    cy.get('[data-testid="manageEntitiesButton"]').should('be.enabled').should('be.visible').and('have.text', 'Manage Entities')
    cy.get('[data-testid="closeButton"]').should('be.enabled').should('be.visible').and('have.text', 'Close Menu')
    cy.get('[data-testid="logOffButton"]').should('be.enabled').should('be.visible').and('have.text', 'Log Off')
  })

  it('navigates to the Manage Entities page', () => {
    cy.get('[data-testid="manageEntitiesButton"]').click()
    cy.url().should('include', '/entities')
    cy.get('[data-testid="menuButton"]').click()
    cy.get('[data-testid="homeButton"]').should('be.enabled')
    cy.get('[data-testid="manageEntitiesButton"]').should('be.disabled')  
  })

  it('closes when the button is clicked', () => {
    cy.get('[data-testid="closeButton"]').click()
    cy.get('[data-testid="closeButton"]').should('not.exist')  
  })

  it('log off the app when the button is clicked', () => {
    cy.get('[data-testid="logOffButton"]').click()
    cy.url().should('include', '/login')  
  })
    
})