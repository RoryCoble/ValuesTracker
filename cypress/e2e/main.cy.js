const dayjs = require('dayjs')
var utc = require("dayjs/plugin/utc");
var timezone = require("dayjs/plugin/timezone");
dayjs.extend(utc)
dayjs.extend(timezone)

describe('Main page', () => {

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
    cy.request({
        method: 'POST',
        url: 'http://localhost:5001/api/connect_user_entity',
        form: true,
        body: {
          userName: 'a',
          entityCode: 'AAAAA'  
        },
    })
    cy.request({
        method: 'POST',
        url: 'http://localhost:5002/dataseed/add_value',
        form: true,
        body: {
          count: 1,
          entityCode: 'AAAAA'  
        },
    }).as('data_point')
  })
  
  beforeEach(() => {
      cy.login('a','a')
  })

  it('should display the expected elements', function () {
    cy.get('[data-testid="pageTitle"]').should('be.visible').and('have.text', 'Entity Tracker')
    cy.get('[data-testid="AAAAA-Header"]').should('be.visible').and('have.text', 'AAAAA')
    cy.get('[class="recharts-responsive-container"]').should('be.visible')
    cy.get('[class="recharts-responsive-container"]').click()
    cy.get('[class="recharts-tooltip-label"]').should('be.visible')
        .and('contain.text', dayjs().tz('GMT').format('ddd, D MMM YYYY H:mm:')).and('contain.text','GMT')
    cy.get('[class="recharts-tooltip-item"]').should('be.visible').and('have.text','value : ' + this.data_point.body)
    cy.get('tspan').should('be.visible')
        .and('contain.text', dayjs().tz('GMT').format('ddd, D MMM YYYY H:mm:')).and('contain.text','GMT')
  })
})