describe('Manage Entities page', () => {

  before(() => {
    let query = 'TRUNCATE TABLE public.users, public.user_entities;'
    const host = Cypress.env('database')
    const port = Cypress.env('database_port')
    let user = 'api'    
    cy.task('databaseQuery', { query, host, port, user })
    query = 'TRUNCATE TABLE public.entities, public.entity_values;'
    user = 'data_seeder'  
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
    cy.request({
        method: 'POST',
        url: Cypress.env('dataseeder_api') + '/dataseed/add_entity',
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
    cy.get('[data-testid="entitySelect"]').should('be.visible')
    cy.get('select[name="entity"] option:selected').invoke('text').should('eq', 'Select Entity')
    cy.get('select[name="entity"]').select(0, { force: true }).invoke('val').should('eq', 'AAAAA')
    cy.get('select[name="entity"]').select(1, { force: true }).invoke('val').should('eq', 'Select Entity')
  })

  it('should allow an Entity to be added and display the entities details', () => {
    cy.get('select[name="entity"]').select(0, { force: true }).invoke('val').should('eq', 'AAAAA')
    cy.get('[data-testid="addEntityButton"]').click()
    cy.get('[data-testid="entitiesTableRow"] td').eq(0).should('be.visible').and('have.text', 'AAAAA')
    cy.get('[data-testid="entitiesTableRow"] td').eq(1).should('be.visible').and('have.text', 'Volatile')
    cy.get('[data-testid="entitiesTableRow"] td').eq(2).should('be.visible').and('have.text', '7.2')  
    cy.get('[data-testid="entitiesTableRow"] td').eq(3).should('be.visible').and('have.text', '7.2')
    cy.get('[data-testid="entitiesTableRow"] td').eq(4).should('be.visible').and('have.text', '7.2')    
  })

})