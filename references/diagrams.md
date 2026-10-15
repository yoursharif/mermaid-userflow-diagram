# Diagrams

Common user flows, ready to adapt. Start from the closest one, rename the nodes for the product, and cut what the request doesn't need. Each diagram shows the happy path plus its usual error and edge branches, followed by its legend.

Read `shapes.md` first. When you cut nodes, cut their legend entries too if no other node uses that shape.

## Login

Email and password sign in, with wrong password, lockout, forgot password and sign up exits.

```mermaid
flowchart TD
  startLogin@{ shape: stadium, label: "Opens login" }
  scrLogin@{ shape: curv-trap, label: "Login screen" }
  inCredentials@{ shape: sl-rect, label: "Enters email and password" }
  actSubmit@{ shape: rect, label: "Taps Sign in" }
  decValid@{ shape: diam, label: "Credentials valid?" }
  decAttempts@{ shape: diam, label: "Under 5 attempts?" }
  scrError@{ shape: curv-trap, label: "Inline error" }
  scrLocked@{ shape: curv-trap, label: "Account locked screen" }
  memSession@{ shape: win-pane, label: "Session token" }
  subReset@{ shape: fr-rect, label: "Password reset flow" }
  subSignup@{ shape: fr-rect, label: "Signup flow" }
  exitHome@{ shape: stadium, label: "Lands on home" }

  startLogin --> scrLogin
  scrLogin -->|Sign in| inCredentials
  scrLogin -->|Forgot password| subReset
  scrLogin -->|Sign up| subSignup
  inCredentials --> actSubmit
  actSubmit --> decValid
  decValid -->|Yes| memSession
  decValid -->|No| decAttempts
  decAttempts -->|Yes| scrError
  decAttempts -->|No| scrLocked
  scrError --> inCredentials
  scrLocked --> subReset
  memSession --> exitHome
```

```mermaid
flowchart TD
  lgTerminator@{ shape: stadium, label: "Terminator: start or end" }
  lgDisplay@{ shape: curv-trap, label: "Display: screen or page" }
  lgProcess@{ shape: rect, label: "Process: step or action" }
  lgDecision@{ shape: diam, label: "Decision: yes or no question" }
  lgManualInput@{ shape: sl-rect, label: "Manual Input: user enters data" }
  lgPredefinedProcess@{ shape: fr-rect, label: "Predefined Process: subflow or other flow" }
  lgInternalStorage@{ shape: win-pane, label: "Internal Storage: session or cache" }

  lgTerminator ~~~ lgDecision
  lgDisplay ~~~ lgManualInput
  lgProcess ~~~ lgPredefinedProcess
  lgDecision ~~~ lgInternalStorage
```

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

## Password reset

Reset by email link. The same confirmation shows whether or not the email is registered, so the screen never reveals who has an account.

```mermaid
flowchart TD
  startForgot@{ shape: stadium, label: "Taps Forgot password" }
  scrForgot@{ shape: curv-trap, label: "Forgot password screen" }
  inEmail@{ shape: sl-rect, label: "Enters email" }
  actSend@{ shape: rect, label: "Taps Send link" }
  decKnown@{ shape: diam, label: "Email registered?" }
  docReset@{ shape: doc, label: "Reset email" }
  scrCheck@{ shape: curv-trap, label: "Check your email screen" }
  waitEmail@{ shape: delay, label: "Waits for email" }
  manOpenEmail@{ shape: trap-t, label: "Opens email app" }
  decLink@{ shape: diam, label: "Link still valid?" }
  scrExpired@{ shape: curv-trap, label: "Link expired screen" }
  scrNewPassword@{ shape: curv-trap, label: "New password screen" }
  inNewPassword@{ shape: sl-rect, label: "Enters new password" }
  decRules@{ shape: diam, label: "Meets password rules?" }
  scrRules@{ shape: curv-trap, label: "Password rules hint" }
  dbUser@{ shape: cyl, label: "Updated user record" }
  exitSignedIn@{ shape: stadium, label: "Signed in" }

  startForgot --> scrForgot
  scrForgot --> inEmail
  inEmail --> actSend
  actSend --> decKnown
  decKnown -->|Yes| docReset
  decKnown -->|No| scrCheck
  docReset --> scrCheck
  scrCheck --> waitEmail
  waitEmail --> manOpenEmail
  manOpenEmail --> decLink
  decLink -->|No| scrExpired
  decLink -->|Yes| scrNewPassword
  scrExpired --> scrForgot
  scrNewPassword --> inNewPassword
  inNewPassword --> decRules
  decRules -->|No| scrRules
  decRules -->|Yes| dbUser
  scrRules --> inNewPassword
  dbUser --> exitSignedIn
```

```mermaid
flowchart TD
  lgTerminator@{ shape: stadium, label: "Terminator: start or end" }
  lgDisplay@{ shape: curv-trap, label: "Display: screen or page" }
  lgProcess@{ shape: rect, label: "Process: step or action" }
  lgDecision@{ shape: diam, label: "Decision: yes or no question" }
  lgManualInput@{ shape: sl-rect, label: "Manual Input: user enters data" }
  lgManualOperation@{ shape: trap-t, label: "Manual Operation: user acts outside the app" }
  lgDelay@{ shape: delay, label: "Delay: waiting" }
  lgDatabase@{ shape: cyl, label: "Database: saved records" }
  lgDocument@{ shape: doc, label: "Document: email, receipt or file" }

  lgTerminator ~~~ lgDecision
  lgDisplay ~~~ lgManualInput
  lgProcess ~~~ lgManualOperation
  lgDecision ~~~ lgDelay
  lgManualInput ~~~ lgDatabase
  lgManualOperation ~~~ lgDocument
```

## Onboarding

First run after sign up: optional tour, permission prompt, a short profile step and a sample project so home isn't empty.

```mermaid
flowchart TD
  startFirst@{ shape: stadium, label: "Opens app first time" }
  scrWelcome@{ shape: curv-trap, label: "Welcome screen" }
  decSkip@{ shape: diam, label: "Skips the tour?" }
  scrTour@{ shape: curv-trap, label: "Three step tour" }
  mergeTour@{ shape: flip-tri, label: " " }
  scrPermission@{ shape: curv-trap, label: "Notification prompt" }
  decAllow@{ shape: diam, label: "Allows notifications?" }
  actRegister@{ shape: rect, label: "Registers device for push" }
  mergePush@{ shape: flip-tri, label: " " }
  inRole@{ shape: sl-rect, label: "Picks role and goals" }
  prepSample@{ shape: hex, label: "Sets up sample project" }
  exitHome@{ shape: stadium, label: "Lands on home" }

  startFirst --> scrWelcome
  scrWelcome --> decSkip
  decSkip -->|No| scrTour
  decSkip -->|Yes| mergeTour
  scrTour --> mergeTour
  mergeTour --> scrPermission
  scrPermission --> decAllow
  decAllow -->|Yes| actRegister
  decAllow -->|No| mergePush
  actRegister --> mergePush
  mergePush --> inRole
  inRole --> prepSample
  prepSample --> exitHome
```

```mermaid
flowchart TD
  lgTerminator@{ shape: stadium, label: "Terminator: start or end" }
  lgDisplay@{ shape: curv-trap, label: "Display: screen or page" }
  lgProcess@{ shape: rect, label: "Process: step or action" }
  lgDecision@{ shape: diam, label: "Decision: yes or no question" }
  lgManualInput@{ shape: sl-rect, label: "Manual Input: user enters data" }
  lgPreparation@{ shape: hex, label: "Preparation: setup before a step" }
  lgMerge@{ shape: flip-tri, label: "Merge: two paths rejoin" }

  lgTerminator ~~~ lgDecision
  lgDisplay ~~~ lgManualInput
  lgProcess ~~~ lgPreparation
  lgDecision ~~~ lgMerge
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

  lgTerminator ~~~ lgDecision
  lgDisplay ~~~ lgManualInput
  lgProcess ~~~ lgPredefinedProcess
  lgDecision ~~~ lgPreparation
  lgManualInput ~~~ lgDelay
  lgPredefinedProcess ~~~ lgDataIO
  lgPreparation ~~~ lgDatabase
  lgDelay ~~~ lgDocument
  lgDataIO ~~~ lgMerge
```

## Empty and error branches

Any screen that loads data. Loading, success, empty, offline and server error, with retry. Add these branches to any flow where a screen fetches something.

```mermaid
flowchart TD
  startOpen@{ shape: stadium, label: "Opens orders" }
  scrLoading@{ shape: curv-trap, label: "Loading skeleton" }
  ioFetch@{ shape: lean-r, label: "Fetches orders" }
  decLoaded@{ shape: diam, label: "Request succeeded?" }
  decOffline@{ shape: diam, label: "Device offline?" }
  scrOffline@{ shape: curv-trap, label: "Offline banner" }
  scrError@{ shape: curv-trap, label: "Error state" }
  actRetry@{ shape: rect, label: "Taps Retry" }
  decHasItems@{ shape: diam, label: "Any orders?" }
  scrEmpty@{ shape: curv-trap, label: "Empty state" }
  actBrowse@{ shape: rect, label: "Taps Start shopping" }
  scrList@{ shape: curv-trap, label: "Orders list" }
  exitShop@{ shape: stadium, label: "Goes to shop" }
  exitList@{ shape: stadium, label: "Views orders" }

  startOpen --> scrLoading
  scrLoading --> ioFetch
  ioFetch --> decLoaded
  decLoaded -->|No| decOffline
  decLoaded -->|Yes| decHasItems
  decOffline -->|Yes| scrOffline
  decOffline -->|No| scrError
  scrOffline --> actRetry
  scrError --> actRetry
  actRetry --> scrLoading
  decHasItems -->|No| scrEmpty
  decHasItems -->|Yes| scrList
  scrEmpty --> actBrowse
  actBrowse --> exitShop
  scrList --> exitList
```

```mermaid
flowchart TD
  lgTerminator@{ shape: stadium, label: "Terminator: start or end" }
  lgDisplay@{ shape: curv-trap, label: "Display: screen or page" }
  lgProcess@{ shape: rect, label: "Process: step or action" }
  lgDecision@{ shape: diam, label: "Decision: yes or no question" }
  lgDataIO@{ shape: lean-r, label: "Data (I/O): data in or out" }

  lgTerminator ~~~ lgDecision
  lgDisplay ~~~ lgDataIO
```
