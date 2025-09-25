describe('Manage Entities page', () => {

  before(() => {
    cy.task('userDb', 'TRUNCATE TABLE public.users, public.user_entities;')
    cy.task('dataseederDb', 'TRUNCATE TABLE public.entities, public.entity_values;')  
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
    cy.request({
        method: 'POST',
        url: 'http://localhost:5002/dataseed/add_entity',
        form: true,
        body: {
          entityCode: 'AAAAA',
          entityType: 'Volatile',
          firstConstant: '7.2',
          secondConstant: '7.2',
          thirdConstant: '7.2'
        },
    })
  })

  beforeEach(() => {
    cy.login('a','a')
    cy.get('[data-testid="menuButton"]').click()
    cy.get('[data-testid="manageEntitiesButton"]').click()  
  })

  it('should display the expected elements', () => {
    cy.get('[data-testid="codeHeader"]').should('be.visible').and('have.text', 'Code')
    cy.get('[data-testid="typeHeader"]').should('be.visible').and('have.text', 'Type')
    cy.get('[data-testid="firstConstantHeader"]').should('be.visible').and('have.text', 'First Constant')
    cy.get('[data-testid="secondConstantHeader"]').should('be.visible').and('have.text', 'Second Constant')
    cy.get('[data-testid="thirdConstantHeader"]').should('be.visible').and('have.text', 'Third Constant')
    cy.get('[data-testid="addEntityButton"]').should('be.visible').and('have.text', 'Add Entity')  
  })

})