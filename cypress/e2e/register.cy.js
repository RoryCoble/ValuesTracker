describe('Register page', () => {
  before(() => {
      cy.task('userDb', 'TRUNCATE TABLE public.users')
  })
    
  it('displays the expected elements', () => {
    cy.visit('/register')
  })
})