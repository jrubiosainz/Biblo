// The runbook's three alerts (CX-147). Each one emails the on-call address, a group that includes the Teams channel
// #returns-assistant-incidents. What to do when one fires is in the runbook, in the section with the alert's name.

param location string
param tags object
param token string

@description('The Log Analytics workspace behind Application Insights, where the App* tables are.')
param logsWorkspaceId string

param onCallEmail string = 'returns-assistant-oncall@contoso.com'

resource onCall 'Microsoft.Insights/actionGroups@2023-01-01' = {
  name: 'ag-support-oncall-${token}'
  location: 'global'
  tags: tags
  properties: {
    groupShortName: 'returns-oc' // 12 characters at most: it's the sender's name in texts
    enabled: true
    emailReceivers: [
      {
        name: 'on-call'
        emailAddress: onCallEmail
        useCommonAlertSchema: true
      }
    ]
  }
}

// Each query returns one row, so the alert compares that row's value with the threshold.
var alerts = [
  {
    name: 'slow-answers'
    displayName: 'Slow answers'
    description: 'The p95 of POST /api/messages is above 8 seconds over 15 minutes. Runbook: Slow answers.'
    severity: 2
    windowSize: 'PT15M'
    query: 'AppRequests | where Name == "POST /api/messages" | summarize p95 = percentile(DurationMs, 95)'
    column: 'p95'
    threshold: 8000
  }
  {
    name: 'errors'
    displayName: 'Errors'
    description: 'More than 10 POST /api/messages failed in 5 minutes. Runbook: Errors.'
    severity: 1
    windowSize: 'PT5M'
    query: 'AppRequests | where Name == "POST /api/messages" and Success == false | summarize failed = count()'
    column: 'failed'
    threshold: 10
  }
  {
    name: 'model-429'
    displayName: '429 from the model'
    description: 'The model answered 429 more than 20 times in 5 minutes. Runbook: 429 from the model.'
    severity: 3
    windowSize: 'PT5M'
    query: 'AppDependencies | where ResultCode == "429" | summarize throttled = count()'
    column: 'throttled'
    threshold: 20
  }
]

resource rules 'Microsoft.Insights/scheduledQueryRules@2023-12-01' = [
  for alert in alerts: {
    name: 'alert-${alert.name}-${token}'
    location: location
    tags: tags
    kind: 'LogAlert'
    properties: {
      displayName: alert.displayName
      description: alert.description
      severity: alert.severity
      enabled: true
      scopes: [logsWorkspaceId]
      evaluationFrequency: 'PT5M'
      windowSize: alert.windowSize
      criteria: {
        allOf: [
          {
            query: alert.query
            metricMeasureColumn: alert.column
            timeAggregation: 'Maximum'
            operator: 'GreaterThan'
            threshold: alert.threshold
            failingPeriods: {
              numberOfEvaluationPeriods: 1
              minFailingPeriodsToAlert: 1
            }
          }
        ]
      }
      autoMitigate: true // resolves itself once the value is back under the threshold
      skipQueryValidation: true // the App* tables only exist once the app has sent something
      actions: {
        actionGroups: [onCall.id]
      }
    }
  }
]
