describe('Register page', () => {
  before(() => {
    cy.task('userDb', 'TRUNCATE TABLE public.users')
  })

  beforeEach(() => {
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
    cy.contains('Cancel').click()
    cy.url().should('include', '/login')
  })    
})