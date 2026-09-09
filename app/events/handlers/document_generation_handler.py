from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.worker_database import WorkerAsyncSessionLocal

from app.modules.finance_layer.invoicing.models import Invoice
from app.modules.system_layer.system.documents.models import Document
from app.modules.system_layer.system.documents.services.document_manager import (
    DocumentManager,
)

from app.modules.finance_layer.invoicing.enums import (
    InvoiceProviderType,
)

from app.modules.system_layer.organisation.models import (
    Company,
    Tenant,
    SystemProvider,
)


async def document_generation_handler(payload: dict):

    document_id = payload.get("document_id")
    invoice_id = payload.get("invoice_id")

    if not document_id or not invoice_id:
        return

    event_context = payload.get("context", {}) or {}

    async with WorkerAsyncSessionLocal() as session:

        # ========================================================
        # DOCUMENT
        # ========================================================

        document_result = await session.execute(
            select(Document)
            .where(
                Document.id == UUID(document_id)
            )
        )

        document = document_result.scalar_one_or_none()

        if not document:
            return

        # ========================================================
        # INVOICE
        # ========================================================

        invoice_result = await session.execute(
            select(Invoice)
            .options(
                # ------------------------------------------------
                # Items
                # ------------------------------------------------
                selectinload(Invoice.items),

                # ------------------------------------------------
                # ERP context
                # ------------------------------------------------
                selectinload(Invoice.tenant),
                selectinload(Invoice.company),
                selectinload(Invoice.branch),

                # ------------------------------------------------
                # Provider / issuer
                # ------------------------------------------------
                selectinload(Invoice.provider_system),
                selectinload(Invoice.provider_company),
                selectinload(Invoice.provider_branch),
                selectinload(Invoice.provider_tenant),

                # ------------------------------------------------
                # Customer
                # ------------------------------------------------
                selectinload(Invoice.customer),
                selectinload(Invoice.paying_customer),

                # ------------------------------------------------
                # Payments
                # ------------------------------------------------
                selectinload(Invoice.payments),
            )
            .where(
                Invoice.id == UUID(invoice_id)
            )
        )

        invoice = invoice_result.scalar_one_or_none()

        if not invoice:
            return

        # ========================================================
        # DETERMINE INVOICE ISSUER
        # ========================================================
        #
        # SYSTEM_PROVIDER:
        #     The ERP/system provider is issuing the invoice.
        #
        # OTHER PROVIDER:
        #     The tenant/company itself is issuing the invoice.
        #
        # ========================================================

        if invoice.provider_type == InvoiceProviderType.SYSTEM_PROVIDER:

            provider = invoice.provider_system

            if not provider:
                raise ValueError(
                    f"System provider not found for invoice "
                    f"{invoice.invoice_number}"
                )

            issuer_company = provider
            issuer_branch = getattr(provider, "branch", None)
            issuer_tenant = getattr(provider, "tenant", None)

        else:

            issuer_company = invoice.company
            issuer_branch = invoice.branch
            issuer_tenant = invoice.tenant

        # ========================================================
        # SAFETY CHECK
        # ========================================================

        if not issuer_company:
            raise ValueError(
                f"Unable to determine invoice issuer company "
                f"for invoice {invoice.invoice_number}"
            )

        # ========================================================
        # DOCUMENT CONTEXT
        # ========================================================

        context = {
            **event_context,

            # ----------------------------------------------------
            # Invoice
            # ----------------------------------------------------

            "invoice": invoice,

            "invoice_number": invoice.invoice_number,

            # ----------------------------------------------------
            # Customer
            # ----------------------------------------------------

            "customer": invoice.customer,

            # ----------------------------------------------------
            # Issuer
            # ----------------------------------------------------

            "company": issuer_company,

            "branch": issuer_branch,

            "tenant": issuer_tenant,

            # ----------------------------------------------------
            # Document metadata
            # ----------------------------------------------------

            "generated_at": None,
        }

        # ========================================================
        # DEBUG
        # ========================================================

        print(
            "\n"
            "============================================================\n"
            "FINAL DOCUMENT JINJA CONTEXT\n"
            "============================================================"
        )

        print("Context keys:")
        print(list(context.keys()))

        print("\nInvoice:")
        print(invoice)

        print("Invoice number:")
        print(invoice.invoice_number)

        print("Provider type:")
        print(invoice.provider_type)

        print("\nIssuer:")
        print("Company:", issuer_company)
        print("Branch:", issuer_branch)
        print("Tenant:", issuer_tenant)

        print("\nCustomer:")
        print(invoice.customer)

        print("\nCurrency:")
        print(invoice.currency)

        print("Subtotal:")
        print(invoice.subtotal)

        print("Discount:")
        print(invoice.discount_amount)

        print("Tax:")
        print(invoice.tax_amount)

        print("Total:")
        print(invoice.total_amount)

        print("Paid:")
        print(invoice.paid_amount)

        print("Balance:")
        print(invoice.balance_amount)

        print("Items:")
        print(len(invoice.items))

        print(
            "============================================================\n"
        )

        # ========================================================
        # GENERATE DOCUMENT
        # ========================================================

        manager = DocumentManager(session)

        await manager.generate(
            document=document,
            context=context,
        )