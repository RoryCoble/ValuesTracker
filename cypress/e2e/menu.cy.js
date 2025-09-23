describe('Page Menu', () => {

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
    
  beforeEach(() => {
    cy.login('a','a')
    cy.get('[aria-haspopup="dialog"]').click()  
  })

  it('displays the expected links', () => {
    cy.contains('Home').should('be.disabled')
    cy.contains('Manage Entities').should('be.enabled')
    cy.contains('Close Menu').should('be.enabled')
    cy.contains('Log Off').should('be.enabled')
  })

  it('navigates to the Manage Entities page', () => {
    cy.contains('Manage Entities').click()
    cy.url().should('include', '/entities')
    cy.get('[aria-haspopup="dialog"]').click()
    cy.contains('Home').should('be.enabled')
    cy.contains('Manage Entities').should('be.disabled')  
  })

  it('closes when the button is clicked', () => {
    cy.contains('Close Menu').click()
    cy.contains('Close Menu').should('not.exist')  
  })

  it('log off the app when the button is clicked', () => {
    cy.contains('Log Off').click()
    cy.url().should('include', '/login')  
  })
    
})