# Documentation claim auditor

An offline tool comparing Markdown promises about structured fields from passports issued by India against static source fingerprints. Requires Python 3.9 or newer; no runtime dependencies. Source is parsed, never executed. The auditor makes no network calls, writes no files, and sends no telemetry.

## Usage

```sh
python3 -m pip install .
indian-passport-extraction-claim-audit audit [repo] --json --fail-on medium
python3 -m indian_passport_extraction_claim_audit audit . --verbose --ignore vendor --ignore build
indian-passport-extraction-claim-audit --version
python3 -m unittest discover
python3 -m build
```

The repository defaults to the current directory. Repeat --ignore with one path prefix per option. The fail threshold accepts high (default) or medium. Exit codes: 0 for no findings reaching the threshold, 2 for findings reaching it, 1 for usage or I/O errors. Version is 0.1.0. JSON provides verdict, findings, claims, evidence, and source_files. A report with MEDIUM findings has verdict FAIL even when the default threshold exits 0.

## Matching and evidence

Only root README.md and Markdown beneath any docs path component supply claims. Blank lines separate paragraphs. Matching lowercases text, expands contractions, replaces hyphens with spaces, collapses whitespace, and uses word boundaries with longest phrases first and alphabetical ties. Denial spans are removed before positive matching. Backtick and tilde fences with up to three leading spaces are excluded; inline code counts.

Symlink files and directories are excluded. Fixtures, docs, and examples components cannot provide evidence. Tests components and test filename conventions supply test evidence separately. Invalid syntax supplies none. Imports and aliases are resolved within one module. Local definitions, assignments, annotated assignments, and context-manager bindings suppress shadowed names. Each route must reside in one module.

A positive promise without production evidence produces HIGH, or MEDIUM when evidence exists only in tests. A denial contradicted by production evidence produces HIGH. One finding is emitted per family. With no source files, positive promises produce HIGH and denials pass.

```text
documented-indian-passport-extraction-claim-false
documented-no-indian-passport-extraction-claim-false
```

The accepted typed route pairs a mindee Client construction with an attribute parse call passing IndianPassportV1 as any positional or keyword argument, as a Name or Attribute. The module must import mindee. Qualified generic calls count as attributes on any base or imported names, including aliases; bare unimported names do not count.

IndianPassportV1 is a 4.x-only fingerprint. The product was removed from the v1 namespace in mindee 5.x. The tool detects the call in source, not the installed SDK version, configured credentials, API availability, or successful execution. Azure Document Intelligence, Mindee, and Veryfi are cloud APIs; detecting source calls does not validate access.

## Limitations and reference vocabulary

Static pattern matching is not semantic judgement. Dead code counts and unsupported alias chains are missed. Verification/KYC, chip or MRZ readers, archival image capture, and classification can cause false positives. Qualified reader/scan calls can refer to chip hardware or MRZ software. Review the code and claim together. Exact wording and the finite denial list constrain matching.

The full vocabulary and required exclusions below are quoted reference material, not capabilities of this auditor.

```text
INDIANPASSPORTEXTRACTION
indian passport extraction
extract indian passport
extracts indian passport
extracting indian passport
extract indian passports
extracts indian passports
extracting indian passports
indian passport parsing
indian passport parser
parse indian passport
parses indian passport
parse indian passports
parses indian passports
indian passport data extraction
extract indian passport data
indian passport field extraction
indian passport document extraction
extract indian passport documents
indian passport reader
indian passport scanning
scan indian passport
scans indian passport
scanning indian passport
indian passport recognition
recognize indian passport
extract indian passport fields
india passport extraction
extract india passport
extracts india passport
extracting india passport
extract india passports
extracts india passports
extracting india passports
india passport parsing
india passport parser
parse india passport
parses india passport
parse india passports
parses india passports
india passport data extraction
extract india passport data
india passport field extraction
india passport document extraction
extract india passport documents
india passport reader
india passport scanning
scan india passport
scans india passport
scanning india passport
india passport recognition

NOINDIANPASSPORTEXTRACTION
no indian passport extraction
does not extract indian passport
does not extract indian passports
does not support indian passport extraction
without indian passport extraction
no indian passport parser
does not parse indian passport
does not parse indian passports
no india passport extraction
does not extract india passport
does not extract india passports
does not support india passport extraction
without india passport extraction
no india passport parser
does not parse india passport
does not parse india passports
indian passport extraction not supported
india passport extraction not supported
does not scan indian passport
does not scan india passport
no indian passport reader
no india passport reader
does not extract indian passport data
does not extract india passport data

Generic call names:
extract_indian_passport
extract_indian_passports
parse_indian_passport
parse_indian_passports
extract_indian_passport_data
parse_indian_passport_data
indian_passport_extraction
indian_passport_reader
read_indian_passport
scan_indian_passport
scans_indian_passport
scanning_indian_passport
indian_passport_parsing
indian_passport_parser
indian_passport_recognition
recognize_indian_passport
indian_passport_field_extraction
indian_passport_document_extraction
extract_indian_passport_documents
get_indian_passport_data
indian_passport_data_extraction
extract_indian_passport_fields
parse_indian_passport_fields
indian_passport_scanning



mindee Client construction + parse call passing IndianPassportV1
(Name exactly IndianPassportV1, or Attribute with attr exactly
IndianPassportV1 such as product.ind.IndianPassportV1 /
mindee.product.ind.IndianPassportV1 /
mindee.product.ind.indian_passport.IndianPassportV1) as any
argument; import gate mindee. IndianPassportV1 IS a 4.x-only
fingerprint (4.22.0 wheel inspected 2026-11-15:
mindee/product/ind/indian_passport/indian_passport_v1.py
defines class IndianPassportV1(Inference), endpoint_name
"ind_passport", endpoint_version "1", exported via
mindee.product.ind and via mindee.product.ind.indian_passport;
its document is "Passport - India API version 1.2" with fields
given_names, surname, id_number, file_number, birth_date,
birth_place, country, gender, issuance_date, issuance_place,
expiry_date, mrz1, mrz2, address1, address2, address3,
legal_guardian, name_of_mother, name_of_spouse,
old_passport_number, old_passport_date_of_issue,
old_passport_place_of_issue, page_number; there is NO
IndianPassportV2 and no TypeIndianPassportV1 form — the 4.22.0
wheel has no mindee/documents module; the 5.4.0 wheel
inspected 2026-11-15 contains NO IndianPassport at all — zero
files matching "indian" anywhere in the wheel, while the
generic PassportV1 survives under mindee/v1/product/passport/,
so the product was removed from the v1 namespace in mindee
5.x). The tool detects the call in source, not the installed
SDK version. A parse call passing any other product
(PassportV1, InternationalIdV2, DriverLicenseV1, IdCardV1,
IdCardV2, HealthcareCardV1, HealthCardV1, InvoiceV4,
ReceiptV5, InvoiceSplitterV1, MultiReceiptsDetectorV1,
FinancialDocumentV1, BankCheckV1, BankAccountDetailsV1,
BankAccountDetailsV2, PayslipV2, PayslipV3, BusinessCardV1,
CustomV1, GeneratedV1, BillOfLadingV1, ResumeV1,
DeliveryNoteV1, CarteGriseV1, EnergyBillV1,
NutritionFactsLabelV1, MaterialCertificateV1, BarcodeReaderV1,
CropperV1, UsMailV2, UsMailV3, or any other) is NOT evidence.
A bare generic extract_passport / parse_passport /
extract_passports / parse_passports / extract_passport_data /
parse_passport_data call with no "indian passport" qualifier
is NOT evidence here (those are the R190 id-document family's
generic names).

## veryfi names (implementation MUST match exactly)

NO veryfi route: the veryfi Python SDK 5.1.0 wheel, inspected
2026-11-15, contains no file or method mentioning "passport"
or "indian" at all — no process_passport /
process_indian_passport / process_indian_passport_url method
exists in the SDK.
NOT evidence: veryfi split_and_process_pdf /
split_and_process_pdf_url (splitting a batched PDF into documents,
the invoice-splitter family's domain); veryfi process_document /
process_any_document and every other veryfi method listed in the
Behaviour section; a call to the non-existent
process_passport / process_indian_passport /
process_indian_passport_url methods (no such methods exist in
the veryfi SDK); a raw HTTP call to
"https://api.veryfi.com/api/v8/partner/documents" (the generic
Veryfi documents endpoint, shared by receipts, invoices, and
other documents — not Indian-passport-specific).

## azure names (implementation MUST match exactly)

NO azure route: Azure Document Intelligence has no
India-specific passport model. The Microsoft Learn v4.0 (GA)
prebuilt-model language-support page and the v4.0 model
catalog, searched 2026-11-15 (catalog listing carried from
R213/R214), list prebuilt-read, prebuilt-layout,
prebuilt-contract, prebuilt-healthInsuranceCard.us,
prebuilt-idDocument, prebuilt-invoice, prebuilt-receipt,
prebuilt-marriageCertificate.us, prebuilt-creditCard,
prebuilt-check.us, prebuilt-payStub.us, prebuilt-bankStatement,
prebuilt-mortgage.us.1003/.1004/.1005/.1008/.closingDisclosure,
prebuilt-tax.us.*, prebuilt-vaccinationCard,
prebuilt-businessCard (deprecated in v4.0), and
prebuilt-document — and no model named "indian passport" or
"india passport".
A begin_analyze_document call with ANY model id is NOT evidence.
prebuilt-idDocument extracts generic passport fields from
passports of many countries (names, document number, dates,
MRZ); it does not extract a file number, old passport details,
a mother's or spouse's name, or address lines, and it is the
R190 id-document family's route.

## google document ai names (implementation MUST match exactly)

NO Google Document AI route: the Document AI processors list /
pretrained overview page, searched 2026-11-15 (carried from
R213/R214), lists pretrained parsers for invoice, expense, bank
statement, pay slip, W2, US driver licence, passport, utility
bill, and identity proofing — the passport parser is generic
(the R190 family's domain), an identity proofing processor
verifies an identity document, it does not extract Indian
passport fields, and there is no India-specific passport
processor, so a process_document call with ANY processor is NOT
evidence.

## eden ai / llamaparse / nanonets / docsumo / other vendor names (implementation MUST match exactly)

NO Eden AI route, by deliberate decision: the standing sibling
rule is that a universal-ai call with ANY model id is NOT
evidence, because the model id is a plain string inside an
arbitrary request payload, not a typed SDK call — the same call
shape serves every Eden AI feature, so there is no fixed static
fingerprint for the call itself. NO LlamaParse route: LlamaParse
is a generative parsing API with no fixed static fingerprint
naming Indian passport extraction. NO Nanonets route: Nanonets
document calls carry an opaque model_id in the URL path (no
fixed fingerprint — the model id is user-configured, not an
Indian passport product). NO Docsumo route: Docsumo uploads go
to a generic endpoint with the document type configured in the
dashboard, not in the call. NO ABBYY Vantage / Rossum / Klippa /
Parseur / Extend route: opaque skill / queue / template /
workflow IDs. NO Textract route: Textract has no Indian passport
extraction operation (analyze_document / analyze_expense /
analyze_id cover generic document, expense, and identity
analysis of one document; analyze_id is the R190 family's
domain). NO PassportEye route: PassportEye read_mrz reads MRZ
lines generically (the R190 family's domain) — reading two MRZ
lines is not extracting an Indian passport's fields. NO generic
OCR route: pytesseract image_to_string or any plain-text
extraction returns raw text, not the structured Indian passport
fields, and has no fixed static fingerprint naming the passport.
NO document classifier route: classifying a document as an
Indian passport returns one label, not the passport's fields.
NO mindee v2 extraction API route: configurable model id, no
fixed fingerprint. NO bare generic extract_passport /
parse_passport route: those are the R190 id-document family's
generic names — a bare "passport" call with no "indian
passport" qualifier cannot be told apart from a generic
passport call. NO mindee PassportV1 route: extracting generic
passport fields is not extracting an Indian passport's
India-specific fields. NO mindee InternationalIdV2 /
DriverLicenseV1 / IdCardV1 / IdCardV2 route: extracting
international ID / driver's license / national identity card
fields is not extracting an Indian passport. NO mindee
HealthCardV1 / HealthcareCardV1 route: extracting health card
fields is not extracting an Indian passport.


Documented matching hazards (honest limitations, also for the README)

- The phrases "indian passport extraction" / "extract indian
  passport" / "indian passport parser" are deliberately
  INDIANPASSPORTEXTRACTION phrases: in document-tool docs they
  name pulling structured fields out of an Indian passport. But
  "indian passport" can also name a passport to verify (identity
  verification, KYC) rather than to extract fields from: a doc
  that means verification, not field extraction, is a false
  positive; the tool flags the claim, only the code decides.
- "indian passport reader" / "india passport reader" are
  deliberately phrases. But a "reader" can also name an
  e-passport chip reader or an MRZ reader (hardware or software
  that reads the chip / MRZ) rather than a field extractor: a doc
  that means chip / MRZ reading, not field extraction, is a
  false positive; the tool flags the claim, only the code decides.
- "scan indian passport" / "scan india passport" are deliberately
  phrases. But "scan" can also name scanning the physical passport
  for archival (producing an image file) rather than extracting
  its fields: a doc that means image capture, not field
  extraction, is a false positive; the tool flags the claim, only
  the code decides.
- "indian passport recognition" / "recognize indian passport" /
  "india passport recognition" are deliberately phrases. But
  "recognition" can also name detecting whether a document IS an
  Indian passport (classification, one label) rather than
  extracting its fields: a doc that means classification, not
  field extraction, is a false positive; the tool flags the claim,
  only the code decides.
- "india passport extraction" / "extract india passport" are
  deliberately phrases: "India passport" is the less idiomatic
  form of the same document name, and docs do use it. But a doc
  that means a passport issued in India as a document to verify
  rather than to extract fields from is a false positive; the
  tool flags the claim, only the code decides.
- IndianPassportV1 extracts the listed fields only (given_names,
  surname, id_number, file_number, birth_date, birth_place,
  country, gender, issuance_date, issuance_place, expiry_date,
  mrz1, mrz2, address1, address2, address3, legal_guardian,
  name_of_mother, name_of_spouse, old_passport_number,
  old_passport_date_of_issue, old_passport_place_of_issue,
  page_number). It carries no visa stamps, no travel history, no
  biometric / fingerprint data, and no chip data. A tool that
  extracts those does so through some other route; this family
  checks for the IndianPassportV1 call, not for those fields.
  Say so in the README.
- A generic `read_indian_passport(` / `scan_indian_passport(` /
  `indian_passport_reader(` call can name an MRZ / chip reader
  rather than an image field extractor: the tool counts the call,
  the claim plus the code decide — and a subprocess call invoking
  an external CLI is NOT evidence by design, so a thin wrapper
  that only calls subprocess fails.
- Mindee `parse` with IndianPassportV1 counts as evidence: the
  product exists in mindee 4.22.0 (wheel inspected 2026-11-15).
  The tool detects the call in source, not whether the call
  succeeds against a current API version. Say so in the README.
- Mindee `parse` with IndianPassportV1 IS a 4.x-only fingerprint:
  mindee 5.x removed the Indian passport product from the v1
  namespace (5.4.0 wheel inspected 2026-11-15 — zero files
  matching "indian" anywhere in the wheel; the generic
  PassportV1 survives under mindee/v1/product/passport/). Say
  so in the README.
- A bare generic `extract_passport(` / `parse_passport(` call
  is NOT detected: those are the R190 id-document family's
  generic names, and a bare "passport" call with no "indian
  passport" qualifier cannot be told apart from a generic
  passport call. Only the qualified names count. Say so in the
  README.
- Mindee `parse` with PassportV1 alone is NOT detected:
  extracting generic passport fields is not extracting an Indian
  passport's India-specific fields (no file number, no old
  passport details, no mother's or spouse's name, no address
  lines), and the generic passport route is the R190 family's
  domain. Say so in the README.
- Mindee `parse` with InternationalIdV2 / DriverLicenseV1 /
  IdCardV1 / IdCardV2 alone is NOT detected: extracting fields
  from an international ID, a driver's license, or a national
  identity card is not extracting an Indian passport, and those
  routes are the id-document family's domain. Say so in the
  README.
- Mindee `parse` with HealthCardV1 / HealthcareCardV1 alone is
  NOT detected: extracting health card fields is not extracting
  an Indian passport. Say so in the README.
- Mindee `parse` with ReceiptV5 / InvoiceV4 / InvoiceSplitterV1 /
  MultiReceiptsDetectorV1 / FinancialDocumentV1 / BankCheckV1 /
  BankAccountDetailsV1 / BankAccountDetailsV2 / PayslipV2 /
  PayslipV3 / NutritionFactsLabelV1 / BusinessCardV1 / CustomV1 /
  GeneratedV1 / BillOfLadingV1 / ResumeV1 / DeliveryNoteV1 /
  CarteGriseV1 / EnergyBillV1 / MaterialCertificateV1 /
  BarcodeReaderV1 / CropperV1 / UsMailV2 / UsMailV3 is NOT
  detected: those are other document types or other operations.
  Say so in the README.
- Azure `begin_analyze_document` with ANY model id is NOT
  detected: Azure Document Intelligence has no India-specific
  passport model (the Learn v4.0 GA prebuilt-model pages list no
  such model, verified 2026-11-15). prebuilt-idDocument extracts
  generic passport fields but no India-specific fields, and it is
  the R190 id-document family's route. Say so in the README.
- Veryfi has NO Indian passport method: the 5.1.0 wheel contains
  no file or method mentioning "passport" or "indian" (verified
  2026-11-15). Veryfi `process_document` /
  `process_any_document` / `split_and_process_pdf` and all other
  veryfi calls are NOT detected. Say so in the README.
- Google Document AI `process_document` / `batch_process_documents`
  with ANY processor is NOT detected: Document AI has no
  India-specific passport processor (the processors list page
  contains no such processor, verified 2026-11-15); the generic
  passport parser is the R190 family's domain. Say so in the
  README.
- Textract `analyze_id` is NOT detected: generic identity
  analysis of one document is not Indian passport extraction,
  and it is the R190 family's domain. Say so in the README.
- PassportEye `read_mrz` is NOT detected: reading MRZ lines
  generically is not extracting an Indian passport's fields, and
  it is the R190 family's domain. Say so in the README.
- Eden AI universal-ai calls with ANY model id are NOT detected:
  the model id is a plain string inside an arbitrary request
  payload, not a typed SDK call, so there is no fixed static
  fingerprint for the call itself. Say so in the README.
- LlamaParse calls are NOT detected: its parsing API is
  generative with no fixed static fingerprint naming Indian
  passport extraction. Say so in the README.
- Nanonets / Docsumo / ABBYY Vantage / Rossum / Klippa / Parseur /
  Extend calls are NOT detected: opaque model / skill / queue /
  template / workflow IDs, or a generic upload endpoint with the
  document type configured outside the call — no fixed fingerprint.
  Say so in the README.
- Generic OCR / table / regex-OCR / CSV calls (pytesseract
  image_to_string, pdfplumber / fitz extract_text, camelot /
  tabula table calls, pandas read_csv / read_excel) are NOT
  detected: plain text or tables are not Indian passport fields.
  Say so in the README.
- Document classifier calls (classify_document,
  is_indian_passport, or any indian-passport-classification call)
  are NOT detected: returning one label is not extracting the
  passport's fields. Say so in the README.
- A hand-rolled extraction from OCR text (`re.search` /
  `re.findall` on extracted text plus manual field assembly,
  no listed call) is NOT detected: the tool requires a listed
  call. Say so in the README.
- The mindee CLI, the veryfi CLI, and any other external
  Indian passport extractor tool invoked through subprocess are NOT
  detected: subprocess calls invoking an external CLI are NOT
  evidence by design. Say so in the README.
- Azure Document Intelligence, Mindee, and Veryfi are cloud APIs:
  the tool detects the client call in source, not whether
  credentials are configured or the call succeeds. Say so in the
  README.
- "extract passport" / "passport extraction" / "extract id
  document" / "id document extraction" claims are NOT in the
  phrase lists: extracting fields from a generic passport or an
  ID document is a different operation from extracting an Indian
  passport — generic passport / ID extraction is the R190
  family's domain. Say so in the README.
- "extract french health card" / "french health card extraction"
  claims are NOT in the phrase lists: extracting a French Carte
  Vitale is a different operation from extracting an Indian
  passport. Say so in the README.
- "extract invoices" / "invoice extraction", "extract receipts" /
  "receipt extraction", "extract financial documents" /
  "financial document extraction", "extract bank statements" /
  "statement extraction", "extract tax forms" / "extract w2 forms",
  "extract pay stubs" / "payslip extraction", "extract us mail" /
  "us mail extraction", "extract contracts" / "contract extraction",
  "extract resumes" / "resume extraction", "extract bills of
  lading" / "bill of lading extraction", "extract delivery notes" /
  "delivery note extraction", "extract carte grises" / "carte
  grise extraction", "extract energy bills" / "energy bill
  extraction", "extract marriage certificates" / "marriage
  certificate extraction", "extract bank account details" / "bank
  details extraction", "extract nutrition facts labels" /
  "nutrition facts label extraction", "extract material
  certificates" / "material certificate extraction", "extract
  health insurance cards" / "health insurance card extraction",
  and "extract bank checks" / "check extraction" claims are NOT
  in the phrase lists: this family covers Indian passport
  extraction only. Say so in the README.
- As with every family: static pattern matching, not semantic
  judgement; dead code counts; alias chains the tracer cannot
  follow are missed; exact phrases only, not semantics; denial
  handling depends on the denial phrase list; each route must sit
  in a single module.

```
