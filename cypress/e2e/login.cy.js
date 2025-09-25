describe('Login page', () => {

  before(() => {
    cy.task('userDb', 'TRUNCATE TABLE public.users')
    cy.request({
        method: 'POST', 
        url: 'http://localhost:5001/api/create_user',
        form: true,
        body: {
          userName : 'a', 
          password : 'a', 
          email : 'a' 
        },
    })
  })

  it('displays the expected elements', () => {
    cy.visit('/')  
    cy.get('[data-testid="pageTitle"]').should('be.visible').and('have.text', 'Login')
    cy.get('[data-testid="usernameInput"]').should('be.visible').and('have.attr', 'placeholder', 'User Name')
    cy.get('[data-testid="passwordInput"]').should('be.visible').and('have.attr', 'placeholder', 'Password')
    cy.get('[data-testid="submitButton"]').should('be.visible').and('have.text', 'Submit')
    cy.get('[data-testid="registerLink"]').should('be.visible').and('have.text', 'Register')
  })

  it('logs in successfully', () => {
    cy.login('a', 'a')
    cy.get('[data-testid="pageTitle"]').should('be.visible').and('have.text', 'Entity Tracker')  
  })

  it('errors on unsuccessful login', () => {
    cy.login('b', 'b')
    cy.get('li[data-sonner-toast]').should('be.visible').and('have.text', 'Login Unsuccessful')  
  })

})