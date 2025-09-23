function register(username, password, email) {
  cy.get('[name="userName"]').type('a')
  cy.get('[name="password"]').type('a')
  cy.get('[name="email"]').type('a')
  cy.get('[type="submit"]').click()
}

describe('Register page', () => {

  beforeEach(() => {
    cy.task('userDb', 'TRUNCATE TABLE public.users')  
    cy.visit('/')
    cy.contains('Register').dblclick()
  })    
    
  it('displays the expected elements', () => {
    cy.get('h1').should('be.visible').and('have.text', 'Register')
    cy.get('[name="userName"]').should('be.visible').and('have.attr', 'placeholder', 'User Name')
    cy.get('[name="password"]').should('be.visible').and('have.attr', 'placeholder', 'Password')  
    cy.get('[name="email"]').should('be.visible').and('have.attr', 'placeholder', 'Email')
    cy.get('[type="submit"]').should('be.visible').and('have.text', 'Submit')
    cy.contains('Cancel').should('be.visible')  
  })

  it('returns to the login page when cancel is clicked', () => {
    cy.contains('Cancel').dblclick()
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