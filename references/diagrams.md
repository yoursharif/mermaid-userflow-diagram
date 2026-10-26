# Diagrams

Two complete single-flow examples, each followed by its legend. Use them as models for structure, branching and naming: rename the nodes for the product and cut what the request doesn't need.

Read `shapes.md` first. Add notes only when the user asks; the one in Checkout is there to show the syntax. When you cut nodes, cut their legend entries too if no other node uses that shape.

## Signup

Email sign up with an existing account check, password rules and email verification.

```mermaid
flowchart TD
  startSignup@{ shape: stadium, label: "Taps Sign up" }
  scrSignup@{ shape: curv-trap, label: "Sign up screen" }
  inDetails@{ shape: sl-rect, label: "Enters name, email, password" }
  actCreate@{ shape: rect, label: "Taps Create account" }
  decRegistered@{ shape: diam, label: "Email already registered?" }
  scrExists@{ shape: curv-trap, label: "Account exists message" }
  decRules@{ shape: diam, label: "Password meets rules?" }
  scrRules@{ shape: curv-trap, label: "Password rules hint" }
  dbUser@{ shape: cyl, label: "New user record" }
  docVerify@{ shape: doc, label: "Verification email" }
  scrCheck@{ shape: curv-trap, label: "Check your email screen" }
  manOpenEmail@{ shape: trap-t, label: "Opens email app" }
  decLink@{ shape: diam, label: "Link still valid?" }
  scrExpired@{ shape: curv-trap, label: "Link expired screen" }
  actResend@{ shape: rect, label: "Taps Resend email" }
  subLogin@{ shape: fr-rect, label: "Login flow" }
  subOnboarding@{ shape: fr-rect, label: "Onboarding flow" }

  startSignup --> scrSignup
  scrSignup --> inDetails
  inDetails --> actCreate
  actCreate --> decRegistered
  decRegistered -->|Yes| scrExists
  decRegistered -->|No| decRules
  scrExists --> subLogin
  decRules -->|No| scrRules
  decRules -->|Yes| dbUser
  scrRules --> inDetails
  dbUser --> docVerify
  docVerify --> scrCheck
  scrCheck --> manOpenEmail
  manOpenEmail --> decLink
  decLink -->|Yes| subOnboarding
  decLink -->|No| scrExpired
  scrExpired --> actResend
  actResend --> docVerify
```

```mermaid
flowchart TD
  lgTerminator@{ shape: stadium, label: "Terminator: start or end" }
  lgDisplay@{ shape: curv-trap, label: "Display: screen or page" }
  lgProcess@{ shape: rect, label: "Process: step or action" }
  lgDecision@{ shape: diam, label: "Decision: yes or no question" }
  lgManualInput@{ shape: sl-rect, label: "Manual Input: user enters data" }
  lgManualOperation@{ shape: trap-t, label: "Manual Operation: user acts outside the app" }
  lgPredefinedProcess@{ shape: fr-rect, label: "Predefined Process: subflow or other flow" }
  lgDatabase@{ shape: cyl, label: "Database: saved records" }
  lgDocument@{ shape: doc, label: "Document: email, receipt or file" }

  lgTerminator ~~~ lgDecision
  lgDisplay ~~~ lgManualInput
  lgProcess ~~~ lgManualOperation
  lgDecision ~~~ lgPredefinedProcess
  lgManualInput ~~~ lgDatabase
  lgManualOperation ~~~ lgDocument
```

## Checkout

Cart to confirmation, with guest checkout, saved address and card, bank check and a declined card.

```mermaid
flowchart TD
  startCart@{ shape: stadium, label: "Taps Checkout" }
  decSignedIn@{ shape: diam, label: "Signed in?" }
  decGuest@{ shape: diam, label: "Continues as guest?" }
  inGuestEmail@{ shape: sl-rect, label: "Enters email" }
  subLogin@{ shape: fr-rect, label: "Login flow" }
  mergeAuth@{ shape: flip-tri, label: " " }
  prepAddress@{ shape: hex, label: "Prefills saved address" }
  scrShipping@{ shape: curv-trap, label: "Shipping step" }
  inAddress@{ shape: sl-rect, label: "Confirms or edits address" }
  scrPayment@{ shape: curv-trap, label: "Payment step" }
  decSavedCard@{ shape: diam, label: "Uses saved card?" }
  inCard@{ shape: sl-rect, label: "Enters card details" }
  mergeCard@{ shape: flip-tri, label: " " }
  actPlace@{ shape: rect, label: "Taps Place order" }
  ioCharge@{ shape: lean-r, label: "Charges card" }
  waitBank@{ shape: delay, label: "Waits for bank check" }
  noteBank@{ shape: brace, label: "May open<br>the bank app" }
  decPaid@{ shape: diam, label: "Payment approved?" }
  scrDeclined@{ shape: curv-trap, label: "Card declined message" }
  dbOrder@{ shape: cyl, label: "New order record" }
  docReceipt@{ shape: doc, label: "Receipt email" }
  scrConfirm@{ shape: curv-trap, label: "Order confirmation" }
  exitPlaced@{ shape: stadium, label: "Order placed" }

  startCart --> decSignedIn
  decSignedIn -->|Yes| mergeAuth
  decSignedIn -->|No| decGuest
  decGuest -->|Yes| inGuestEmail
  decGuest -->|No| subLogin
  inGuestEmail --> mergeAuth
  mergeAuth --> prepAddress
  prepAddress --> scrShipping
  scrShipping --> inAddress
  inAddress --> scrPayment
  scrPayment --> decSavedCard
  decSavedCard -->|Yes| mergeCard
  decSavedCard -->|No| inCard
  inCard --> mergeCard
  mergeCard --> actPlace
  actPlace --> ioCharge
  ioCharge --> waitBank
  waitBank --> decPaid
  noteBank -.- waitBank
  decPaid -->|No| scrDeclined
  decPaid -->|Yes| dbOrder
  scrDeclined --> scrPayment
  dbOrder --> docReceipt
  docReceipt --> scrConfirm
  scrConfirm --> exitPlaced
```

```mermaid
flowchart TD
  lgTerminator@{ shape: stadium, label: "Terminator: start or end" }
  lgDisplay@{ shape: curv-trap, label: "Display: screen or page" }
  lgProcess@{ shape: rect, label: "Process: step or action" }
  lgDecision@{ shape: diam, label: "Decision: yes or no question" }
  lgManualInput@{ shape: sl-rect, label: "Manual Input: user enters data" }
  lgPredefinedProcess@{ shape: fr-rect, label: "Predefined Process: subflow or other flow" }
  lgPreparation@{ shape: hex, label: "Preparation: setup before a step" }
  lgDelay@{ shape: delay, label: "Delay: waiting" }
  lgDataIO@{ shape: lean-r, label: "Data (I/O): data in or out" }
  lgDatabase@{ shape: cyl, label: "Database: saved records" }
  lgDocument@{ shape: doc, label: "Document: email, receipt or file" }
  lgMerge@{ shape: flip-tri, label: "Merge: two paths rejoin" }
  lgCurlyBraceNote@{ shape: brace, label: "Curly Brace Note: comment on a node" }

  lgTerminator ~~~ lgDecision
  lgDisplay ~~~ lgManualInput
  lgProcess ~~~ lgPredefinedProcess
  lgDecision ~~~ lgPreparation
  lgManualInput ~~~ lgDelay
  lgPredefinedProcess ~~~ lgDataIO
  lgPreparation ~~~ lgDatabase
  lgDelay ~~~ lgDocument
  lgDataIO ~~~ lgMerge
  lgDatabase ~~~ lgCurlyBraceNote
```
