---
title: Credit Trust and Equipment Financing
aliases:
  - Credit Trust
  - Erbium Equipment Financing
type: house-rules
status: playtest
version: "0.1"
tags:
  - erbium-industries
  - player-resource
  - economy
  - house-rules
---

# Credit Trust and Equipment Financing

> [!quote] Erbium Industries LLC — Personnel Financial Services
> Erbium-approved financing keeps essential equipment within reach of qualified personnel. All issued property remains subject to the terms of its agreement.

## Quick Reference

| Rule | How it works |
| --- | --- |
| **Credit Trust** | A rating from **1 to 5**, calculated from your level, liquid credits, and Society proficiency. |
| **Credit limit** | Your level's reference reserve × your Credit Trust. |
| **Shared limit** | Leased equipment and installment purchases use the same limit. |
| **Lease** | Rent reusable equipment for **5% of its listed price per 10,080 offsets**, accruing throughout its use. |
| **Installments** | Buy an item through payments of **10% of the original amount financed per billing date**, until fully paid. |
| **Billing cycle** | **10,080 offsets**, equal to seven standard days. Each account has one scheduled billing date. |
| **Returning leased gear** | Stops further rent. Pay any remaining accrued rent; bad condition also incurs the item's **full listed price**. |
| **Rewards** | Contract compensation and bonuses provide credits. Your rating changes through account reviews. |

Financing remains subject to item availability and the seller's participation in the program.

## 1. Calculate Your Credit Trust

At an account review, find your **reference reserve** by character level. This number is a benchmark for assessment; it is not money added to your account.

| Level | Reference reserve | Level | Reference reserve |
| ---: | ---: | ---: | ---: |
| 1 | 150 credits | 11 | 5,000 credits |
| 2 | 200 credits | 12 | 7,000 credits |
| 3 | 250 credits | 13 | 10,000 credits |
| 4 | 300 credits | 14 | 15,000 credits |
| 5 | 500 credits | 15 | 22,500 credits |
| 6 | 800 credits | 16 | 32,500 credits |
| 7 | 1,250 credits | 17 | 50,000 credits |
| 8 | 1,800 credits | 18 | 75,000 credits |
| 9 | 2,500 credits | 19 | 120,000 credits |
| 10 | 3,500 credits | 20 | 200,000 credits |

**Credit Trust = 1 + reserve bonus + Society bonus.** Choose one row from each category below.

| Category | Your situation at the review | Bonus |
| --- | --- | ---: |
| Credits | Less than half your reference reserve | +0 |
| Credits | At least half your reference reserve, but less than the full reserve | +1 |
| Credits | At least your full reference reserve | +2 |
| Society | Untrained | +0 |
| Society | Trained or expert | +1 |
| Society | Master or legendary | +2 |

**Liquid credits** are credits you own and can spend. Equipment value, available financing, borrowed money, and someone else's account balance do not count as liquid reserves. Society represents your ability to navigate financial procedures and identify programs for which you qualify; no skill check is required.

| Credit Trust | Classification | Credit limit |
| ---: | --- | --- |
| 1 | Restricted | Reference reserve × 1 |
| 2 | Limited | Reference reserve × 2 |
| 3 | Standard | Reference reserve × 3 |
| 4 | Preferred | Reference reserve × 4 |
| 5 | Priority | Reference reserve × 5 |

### Account Reviews

Review your account when it is opened, at each scheduled billing date, and after a contract payout. You may also request a review after gaining a level. At billing, apply payments first and assess the credits you still have afterward. Record the approved limit until the next review.

Ordinary purchases and payments do not immediately change your rating. A new level changes the reference reserve at review; use the new reserve to calculate both the reserve bonus and the limit. Spending below a threshold can lower your next rating, while receiving a bonus can raise it.

If your commitments exceed a newly reduced limit, existing agreements continue and further financing is unavailable until you have enough room. Account suspension is a separate status: it blocks new financing while preserving the calculated rating.

> [!example] Level-1 Assessment
> Your reference reserve is **150 credits**. You own **100 liquid credits** and are **trained in Society**.
>
> Credit Trust = 1 + 1 for reserves + 1 for Society = **3**.
>
> Credit limit = 150 × 3 = **450 credits**.

## 2. Check Available Financing

Your approved limit applies to the total value committed across all your agreements. Multiple cards or purchases use the same account.

| Commitment | Amount using your limit |
| --- | --- |
| Active lease | The item's full listed price, recorded at checkout. Rent payments do not reduce this amount. |
| Installment purchase | The remaining unpaid purchase balance, including any overdue installments. |
| Unpaid return-condition charge | The unpaid part of the assessed listed-price charge. |

**Available financing = credit limit − total committed value**, with a minimum of zero.

Before entering a new agreement, its commitment must fit within your available financing, and your account must permit new borrowing. Paying liquid credits toward a purchase upfront reduces the amount financed. The recorded price and rate of an existing agreement remain fixed when your level or rating changes.

Overdue rent is tracked under **Past Due**. Overdue purchase installments are already included in their purchase balances, so do not add them to committed value again.

## 3. Leasing Reusable Equipment

A lease permits you to use an item while Erbium retains ownership. Reusable tools, weapons, armor, and other approved durable equipment can be leased. Ammunition, consumables, and other expendable goods must be purchased.

| Lease term | Rule |
| --- | --- |
| Recorded value | The item's full listed price at checkout. |
| Rental rate | **5% of that price per 10,080 offsets.** |
| Accrual | Rent accrues from the checkout stamp until the return stamp. |
| Collection | Accrued rent is collected at scheduled billing dates; any unbilled remainder is due on return. |
| Ownership | The item remains Erbium property throughout the lease. |
| Duration | Payments continue for as long as you keep the item. |
| Rent already paid | Covers previous use and does not count toward ownership or a damage charge. |

**Accrued rent = listed price × 0.05 × unbilled offsets used ÷ 10,080.**

At each bill or return, charge only the time since checkout or the last billed-through stamp, whichever is later. Once a period has been billed, record its end stamp even if the bill is unpaid; the charge becomes arrears and must not be billed a second time.

Keep fractional rent during the calculation. Add the lease charges being settled together and round the resulting rental subtotal up to the next whole credit once. There is no rounding or separate minimum charge for every offset.

### Returning Leased Equipment

Record the return stamp when the item is accepted back. Rent stops at that stamp, even if inspection or payment happens afterward.

| Return condition | Amount due | Credit-limit effect |
| --- | --- | --- |
| Acceptable condition | Unpaid rent and any unbilled rent through the return stamp | Release the item's full listed value. |
| Bad condition | The same rent, **plus the full listed price** | Release the lease commitment; any unpaid condition charge uses the limit until paid. |

**Bad condition** means broken, missing essential components, or functionally impaired beyond ordinary wear. Cosmetic wear and damage recorded at checkout are acceptable. You may repair an item before returning it, subject to any repair restrictions disclosed in its agreement. The GM resolves uncertain condition assessments.

The condition charge does not transfer ownership to you: the item has been returned to Erbium. Paying that charge does not create further rent. A lost item has not been returned; contact Erbium to arrange recovery or a settlement that formally closes the lease.

> [!important] Renting Beyond the Item's Value
> Lease payments have no cumulative price cap. If you keep an item long enough to pay more than its listed price in rent, the lease continues at the same rate until you return it or agree to a separate settlement.

## 4. Installment Purchases

Installments spread a purchase across recurring payments. Reusable items and consumables both qualify when the vendor offers financing.

| Purchase term | Rule |
| --- | --- |
| Amount financed | Purchase price minus any upfront payment. |
| Regular installment | **10% of the original amount financed**, rounded up to a whole credit. |
| Due date | Each scheduled account billing date, beginning with the first date disclosed at purchase. |
| Final payment | Only the amount still owed. |
| Total purchase payments | The agreed purchase price, including any upfront payment. |
| Interest and financing fees | None under these rules. |
| Early repayment | You may pay extra or clear the balance at any time without a penalty. |
| Ownership | A reusable item becomes yours when its purchase balance reaches zero. |
| Consumables | Using them does not cancel their remaining purchase balance. |

The regular installment is calculated from the **original amount financed**. It does not shrink each time you pay. Any overdue installments are collected in addition to the next newly due installment, without charging more than the remaining purchase balance in total.

Early payments reduce the balance and shorten the repayment period. They do not postpone the next scheduled installment while a balance remains. A fully paid item releases its remaining commitment and generates no further installments.

Leased equipment cannot be sold without authorization. An authorized sale or return of an item still being purchased applies its agreed buyback value to that item's unpaid balance first; any shortfall remains owed. A lease return simply ends the lease under its return terms and produces no sale proceeds.

## 5. Lease or Purchase?

For an item listed at **200 credits**, with no upfront purchase payment:

| Arrangement | Payment | Result |
| --- | ---: | --- |
| Lease for 5,040 offsets, then return in acceptable condition | 5 credits | Equipment returned; no further rent. |
| Lease for 10,080 offsets, then return in acceptable condition | 10 credits | Equipment returned; no further rent. |
| Lease for 10 full billing cycles | 100 credits total | Still leased; rent continues while retained. |
| Lease for 25 full billing cycles | 250 credits total | Still leased; rent continues while retained. |
| Purchase through installments | 20 credits per billing date, for 10 payments | Paid in full at 200 credits; item owned. |
| Lease for 5,040 offsets, then return in bad condition | 5 rent + 200 condition charge = **205 credits** | Equipment returned; no further rent. |

## 6. Billing and Missed Payments

All agreements on an account share one recurring due stamp. The first account due stamp is set **10,080 offsets after the account opens**; subsequent due stamps are another 10,080 offsets apart. A new agreement joins the next scheduled bill. Its first due stamp must be shown before you accept it.

Lease charges reflect the actual time used, including partial cycles. Installments are whole scheduled payments and are not prorated when purchased shortly before a billing date. Returning a lease between billing dates settles its remaining rent immediately and leaves the account's regular schedule unchanged.

| At a billing date | What to do |
| --- | --- |
| Calculate the statement | Add newly accrued rent and newly due installments to unpaid previous charges. Newly due installments cannot exceed the purchase balance that has not already fallen due. |
| Make a payment | Subtract the credits paid from liquid credits. Apply them to the oldest unpaid charges first; for charges due together, choose which to settle. |
| Update agreements | Purchase payments reduce purchase balances. Rent pays for use. Payments toward condition charges reduce those charges. |
| Check arrears | Record unpaid amounts as Past Due. Each unpaid charge appears only once. |
| Assess standing | Apply the escalation below and review the credit rating using the remaining liquid credits. |
| Advance the deadline | Add **10,080 offsets** to the scheduled due stamp. |

**Past Due is the overdue portion of amounts already owed.** It is a tracking total, not another fee added on top of those amounts. Return charges that are unpaid when due enter Past Due immediately; account escalation is assessed on the regular billing dates.

### Escalation

| Consecutive billing dates ending with an overdue balance | Account status | Consequence |
| ---: | --- | --- |
| 0 | Current | Normal access, subject to the credit limit. |
| 1 | Notice | Notice of arrears. Settle the overdue amount to return to Current. |
| 2 | Suspended | New leases and financing are declined. Existing agreements and payments continue. |
| 3 or more | Collections | Erbium demands settlement, surrender of leased equipment, or an explicitly offered recovery assignment. Enforcement is resolved in play. |

Clearing all overdue charges resets the missed-payment count and removes financial suspension. Any collection action already in progress is resolved with the collector. A payment failure does not automatically disable equipment or create a combat penalty. No additional interest or late fees accrue under this version of the rules.

The GM announces billing dates crossed during travel or downtime. Review them in chronological order, with opportunities to account for payments at each date. If several dates pass with no payments, combine the calculation and apply the resulting status once at the table.

> [!note] Relay Coverage
> Due dates follow PES, including while you are off-stamp. Record attempted payments and any outage. Offline-payment acceptance, extensions, or a disputed corporate record are handled by the GM and the agreement's terms; disconnection alone neither pays a bill nor closes a lease.

## 7. Worked Account Example

A level-1 character has **100 liquid credits**, **trained Society**, and an approved **Credit Trust of 3**. Their reference reserve is 150 credits and their limit is **450 credits**.

| Agreement | Recorded price | Current commitment | Payment for a full cycle |
| --- | ---: | ---: | ---: |
| Leased scanner | 150 | 150 | 7.5 rent, rounded with the statement's rental subtotal |
| Medical supplies purchased on installments | 90 | 90 | 9 |
| **Total** | — | **240** | **17 credits after rounding rent** |

Before payment, available financing is **450 − 240 = 210 credits**. The supplies may be used immediately; the purchase balance remains until paid.

After one full cycle, the character pays **17 credits**: 8 rent and 9 toward the supplies. Liquid credits fall to **83**, the supplies' balance falls to **81**, and the scanner still occupies **150** credits. At review, 83 is still at least half the 150-credit reserve, so Trust remains 3. Available financing is now **450 − 231 = 219 credits**.

If the scanner is returned immediately after that bill in acceptable condition, its 150-credit commitment is released and no further rent accrues. The only remaining commitment is the supplies' 81-credit balance.

## 8. Copyable Account Tracker

Record the approved limit at review. Update the agreement rows when you borrow, return, buy, or pay. The account summary is a total of those rows; it does not create additional debts.

| Account field | Value |
| --- | --- |
| Account holder | |
| Level / reference reserve | |
| Liquid credits | |
| Society proficiency | |
| Credit Trust / approved limit | |
| Total committed / available financing | |
| Next due stamp | |
| Expected payment at next due stamp | |
| Past Due / consecutive missed billing dates | |
| Status | Current |

### Active Leases

| Item | Listed price | Checkout stamp | Billed through | Rent already billed but unpaid | Checkout condition |
| --- | ---: | --- | --- | ---: | --- |
| | | | | 0 | |

On return, settle the final unbilled rent, remove the item from active leases, and retain a short return record. Transfer any unpaid rent or condition charge to the table below. Record the return stamp so no further rent is charged.

### Installment Purchases

| Item | Original amount financed | Remaining balance | Regular installment | Overdue portion of balance |
| --- | ---: | ---: | ---: | ---: |
| | | | | 0 |

### Unpaid Charges from Closed Leases

| Returned item | Return stamp | Unpaid rent | Unpaid condition charge |
| --- | --- | ---: | ---: |
| | | 0 | 0 |

**Past Due** is the sum of billed-but-unpaid rent, overdue purchase portions, and unpaid charges from closed leases. A purchase's overdue portion is included in its remaining balance. Only the unpaid condition-charge column from closed leases counts toward committed value; its rent remains tracked as arrears.

---

*Playtest version 0.1. Reference reserves reproduce the Currency column of the Starfinder Second Edition GM Core Character Wealth table, page 61. Credit ratings, financing limits, payment rates, and contract procedures in this document are campaign house rules.*
