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
    cy.get('h1').should('be.visible').and('have.text', 'Login')
    cy.get('[name="userName"]').should('be.visible').and('have.attr', 'placeholder', 'User Name')
    cy.get('[name="password"]').should('be.visible').and('have.attr', 'placeholder', 'Password')
    cy.get('[type="submit"]').should('be.visible').and('have.text', 'Submit')
    cy.contains('Register').should('be.visible')  
  })

  it('logs in successfully', () => {
    cy.login('a', 'a')
    cy.get('h1').should('be.visible').and('have.text', 'Entity Tracker')  
  })

  it('errors on unsuccessful login', () => {
    cy.login('b', 'b')
    cy.get('li[data-sonner-toast]').should('be.visible').and('have.text', 'Login Unsuccessful')  
  })

})