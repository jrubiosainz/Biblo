-- Courier pickups booked for the next 14 days, by day and slot, against what Fabrikam Logistics agreed to collect
-- during the pilot: 15 pickups a slot. Pablo checks it every morning until CX-152 connects the returns API to the
-- courier. dbo.pickups comes from the returns API with the Copy returns pipeline at 06:00, so a pickup booked today
-- shows up tomorrow. Slots are text like '16:00–18:00', which sorts in time order.

DECLARE @per_slot int = 15;

SELECT
    pickup_date,
    DATENAME(weekday, pickup_date) AS weekday,
    slot,
    COUNT(*) AS pickups,
    @per_slot - COUNT(*) AS left_in_slot,
    SUM(CASE WHEN fee_eur > 0 THEN 1 ELSE 0 END) AS paid_by_customer,  -- €4.95, when they no longer need it
    CASE WHEN COUNT(*) > @per_slot THEN 'call Fabrikam Logistics' ELSE '' END AS action
FROM dbo.pickups
WHERE status = 'booked'
    AND pickup_date >= CAST(GETDATE() AS date)
    AND pickup_date < DATEADD(day, 14, CAST(GETDATE() AS date))
GROUP BY pickup_date, slot
ORDER BY pickup_date, slot;
