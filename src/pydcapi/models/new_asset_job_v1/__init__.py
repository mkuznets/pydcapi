# generated by datamodel-codegen:
#   filename:  new_asset_job_v1.json

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import AnyUrl, BaseModel, ConfigDict


class AssetResult(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        frozen=True,
    )
    mimetype: str
    """
    The IANA Mime type
    """
    name: str
    """
    the new asset
    """
    uri: str
    """
    Asset URI reference
    """


class Error(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        frozen=True,
    )
    code: str
    """
    **Code** | **Description** | **Affected Operations** | **Corrective Action**
    --- | --- | --- | ---
    QuotaExceeded | The operation failed because some aspect of the user quota on the relevant storage cloud was exceeded. | All | Increase quotas or reduce usage.
    CloudError | An error from the supporting cloud storage | All | Report Error to Adobe.
    UnsupportedMimeType | Input file type cannot be converted to PDF | createpdf, createpdf_from_html | Cannot convert this document.
    DocumentCorrupted | The file appears to be corrupted and cannot be converted. | exportpdf, pdf_actions | Cannot convert this document.
    PDFIsPortfolio | This file cannot be converted because it is a portfolio. | exportpdf | Extract Portfolio contents and process them individually.
    PDFNoTables | This file cannot be converted as a spreadsheet because it does not appear to contain a table. | exportpdf | Cannot convert this document.
    SourceIsEncrypted | This file is encrypted and cannot be converted. | All | Remove document encryption.
    TimeOut | This file could not be converted because it took too long to convert. | All | Simplify content.
    PDFIsEncryptedOrForm | Source PDF is either encrypted or is a Form | exportpdf, combinedpdf | Remove document encryption or flatten the XFA Form.
    PDFPolicyProtected | Source PDF is policy protected and cannot be opened. | exportpdf, pdf_actions | Remove Policy protection.
    Unknown | An unknown conversion error has occurred.  Please report the error details. | All | Document cannot be converted. Report Error to Adobe.
    SourceIsEmpty | The file being converted was a zero length file. | All  | Cannot convert this document.
    SourceTooLarge  | The file being converted was greater than 100 MB in size.  | All | Cannot convert this document.
    InvalidPageRange | The page range specified for combine was invalid. Either invalid range syntax, bad page references, or results in a PDF with too many pages relative to the input PDF(s). | exportpdf, pdf_actions | Fix input parameters.
    GeneralFormError | Error processing a Form File. | Form processing | Cannot convert this document.
    PDFIsCertified | PDF cannot be processed due to document certification. | pdf_actions, exportpdf | Remove document certification.
    PDFIsXFAForm | PDF cannot be processed because it is XFA-based. | pdf_actions, exportpdf  | Flatten the XFA-PDF to a regular PDF file.
    InvalidHTMLInput | Cannot create PDF from the provided HTML. | createpdf_from_html  | Look at the message for hints on how to correct the HTML zip package.
    MaxPagesSupported | This request has exceeded the maximum number of pages | createpdf, pdf_actions | Use file with less than 100 pages.
    FileCountLimitExceeded | This request has exceeded the maximum number of files that can be combined | pdf_actions | Use multiple requests to combine large numbers of files.
    InputMustBePDF | Input file(s) for this request must have a mime type: application/pdf | pdf_actions, exportpdf | Convert file(s) to PDF before attempting this operation.
    InvalidDestination | This asset cannot be exported to the specified desitnation provider. | export | Check discovery.source_options for allowed destinations.
    InvalidAssetOrigins | Unable to mix assets from multiple origins. | pdf_actions, export | Only perform operations with assets from the same origin.
    ExternalAssetError | Unable to complete the request operation with the specified external asset(s). | All | Review error message for details on the external asset failure.
    DuplicateName | You can't have two things with the same name in the same folder. | All | Use a different name.
    FileNotQualified | This PDF file will not convert well into fully taggged pdf | pdf_actions | View file in classic view 
    IncompatibleClientVersion | The version specified in the client_version field is not supported by the server. | pdf_actions | Render file in classic view and, optionally, prompt user to upgrade client software.
    UserPasswordLengthExceeded | User password too long | pdf_actions | Keep password length less than 128 characters.
    OwnerPasswordLengthExceeded | Owner password too long. | pdf_actions | Keep password length less than 128 characters.
    InvalidPermission | The document access permission is either invalid or not supported. | pdf_actions | Use valid values for permissions.	
    InvalidContentToEncrypt | Specified content encryption setting is invalid. | pdf_actions | Use a valid type for the content to encrypt.
    InvalidEncryptionAlgorithm | Encryption algorithm is either invalid or not supported. | pdf_actions | Use a valid encryption algorithm.
    SameUserAndOwnerPassword | User and owner password can not be same. | pdf_actions | Provide different values for user and owner passwords.
    PDFIsSignedOrCertified| 	Source PDF file is either digitally signed or protected by a certificate.| 	pdf_actions | 	Remove digital signatures.
    PDFHasFileAttachments| 	PDF document containing file attachments is not supported.| 	pdf_actions |  Remove file attachments.
    PDFIsNotPasswordProtected| 	Source PDF file is not password protected.| 	pdf_actions | Cannot remove security from this document.
    InvalidPassword| 	The password is not authorized to remove the security.| 	pdf_actions | Provide valid password.
    InvalidSplitParams| Zero or more than one params provided for splitting PDF document. |  splitpdf | Provide valid params.
    InvalidSplitPageRanges | The page range specified for split was invalid. | splitpdf | Fix input parameters.
    MaxOutputFilesSupported | The input PDF cannot be split into more than 20 output PDFs. | splitpdf | Reduce the number of split points.

    """
    message: str
    """
    An English language string that contains more information about the error. This is not intended as information to be presented to an end user, but will instead be helpful for logging and debugging.
    """
    status: Optional[int] = None
    """
    The http status code.
    """


class MultipleAssetResultItem(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        frozen=True,
    )
    mimetype: str
    """
    The IANA Mime type
    """
    name: str
    """
    the new asset
    """
    uri: str
    """
    Asset URI reference
    """


class Model(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        frozen=True,
    )
    asset_result: Optional[AssetResult] = None
    """
    If the status is 'done', this will contain the details of the new asset
    """
    error: Optional[Error] = None
    """
    If the status is 'failed', this will contain the error details
    """
    job_uri: Optional[AnyUrl] = None
    """
    If the job state is either 'queued' or 'in progress', use this URI to poll for completion.  Note that this method should be called only after the interval specified in: retry_interval
    """
    multiple_asset_result: Optional[List[MultipleAssetResultItem]] = None
    """
    If the status is 'done', this will contain the details of the new assets list
    """
    progress: Optional[float] = None
    """
    A value from zero to one hundred indicating the job completion progress
    """
    retry_interval: Optional[int] = None
    """
    If the status is 'queued' or 'in progress' this specifies the number of milliseconds to wait before re-querying the job status
    """
    status: Literal['done', 'queued', 'in progress', 'failed']
    """
    job status
    """
