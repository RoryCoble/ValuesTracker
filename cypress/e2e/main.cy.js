describe('Main page', () => {
    
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
    cy.request({
        method: 'POST',
        url: Cypress.env('dataseeder_api') + '/dataseed/add_entity',
        form: true,
        body: {
          entityCode: 'BBBBB',
          entityType: 'Volatile',
          firstConstant: '1.2',
          secondConstant: '1.2',
          thirdConstant: '1.2'
        },
    })  
    cy.request({
        method: 'POST',
        url: Cypress.env('api') + '/api/connect_user_entity',
        form: true,
        body: {
          userName: 'a',
          entityCode: 'AAAAA'  
        },
    })
    cy.request({
        method: 'POST',
        url: Cypress.env('api') + '/api/connect_user_entity',
        form: true,
        body: {
          userName: 'a',
          entityCode: 'BBBBB'  
        },
    })  
    cy.request({
        method: 'POST',
        url: Cypress.env('dataseeder_api') + '/dataseed/add_value',
        form: true,
        body: {
          count: 1,
          entityCode: 'AAAAA'  
        },
    }).as('data_point_AAAAA')
    cy.request({
        method: 'POST',
        url: Cypress.env('dataseeder_api') + '/dataseed/add_value',
        form: true,
        body: {
          count: 1,
          entityCode: 'BBBBB'  
        },
    }).as('data_point_BBBBB')  
  })
  
  beforeEach(() => {
      cy.login('a','a')
  })

  it('should display the expected elements', function () {
    cy.get('[data-testid="pageTitle"]').should('be.visible').and('have.text', 'Entity Tracker')
    cy.get('[data-testid="AAAAA-Header"]').should('be.visible').and('have.text', 'AAAAA')
    cy.xpath('//h1[@data-testid="Totals-Header"]/following::div[1]/*[@class="recharts-responsive-container"]').should('be.visible')
    cy.xpath('//h1[@data-testid="Totals-Header"]/following::div[1]/*[@class="recharts-responsive-container"]').click()
    cy.get('[class="recharts-tooltip-label"]').should('be.visible').and('contain.text', '1')
    cy.get('[class="recharts-tooltip-item"]').should('be.visible').and('contain.text','AAAAA : ' + this.data_point_AAAAA.body)
    cy.get('[class="recharts-tooltip-item"]').should('be.visible').and('contain.text','BBBBB : ' + this.data_point_BBBBB.body)  
    cy.get('tspan').should('be.visible').should('be.visible').and('contain.text', '0')
    cy.xpath('//h1[@data-testid="AAAAA-Header"]/following::*[@class="recharts-responsive-container"][1]').should('be.visible')
    cy.xpath('//h1[@data-testid="AAAAA-Header"]/following::*[@class="recharts-responsive-container"][1]').click()
    cy.get('[class="recharts-tooltip-label"]').should('be.visible').and('contain.text', '1')
    cy.get('[class="recharts-tooltip-item"]').should('be.visible').and('contain.text','value : ' + this.data_point_AAAAA.body)  
    cy.xpath('//h1[@data-testid="AAAAA-Header"]/following::*[@class="recharts-responsive-container"][2]').should('be.visible')
    cy.xpath('//h1[@data-testid="AAAAA-Header"]/following::*[@class="recharts-responsive-container"][2]').click()
    cy.get('[class="recharts-tooltip-label"]').should('be.visible').and('contain.text', '1')
    cy.get('[class="recharts-tooltip-item"]').should('be.visible').and('contain.text','value : ' + this.data_point_BBBBB.body)    
  })
})