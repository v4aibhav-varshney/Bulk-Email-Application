import os
import fitz
from reportlab.pdfgen import canvas
from pdfrw import PdfReader, PdfWriter, PageMerge
from pylovepdf.ilovepdf import ILovePdf

def encrypt_pdf(owner_pass, user_pass, path, saved_name):
    """
    Encryption function using PyMuPDF which performs AES-256 bit encryption and saves the file
    :param owner_pass: Sets the owner password
    :param user_pass: Sets the user password
    :param path: The path to the file to be encrypted
    :param saved_name: The name of the final PDF
    :return: None
    """

    perm = int(
        fitz.PDF_PERM_ACCESSIBILITY
        | fitz.PDF_PERM_PRINT
        | fitz.PDF_PERM_COPY
        | fitz.PDF_PERM_ANNOTATE
    )

    encrypt_meth = fitz.PDF_ENCRYPT_AES_256
    doc = fitz.open(path)
    doc.save(
        saved_name,
        encryption=encrypt_meth,
        owner_pw=owner_pass,
        user_pw=user_pass,
        permissions=perm,
    )

def create_annotation(wmark_file, rec_name):

    c = canvas.Canvas(wmark_file)
    c.drawString(30, 820, rec_name)
    c.showPage()
    c.save()

def merge_annotation(inpfn, wmarkfn, underneath=False):
    outfn = 'Watermarked_' + os.path.basename(inpfn)

    # Open both the source files
    wmark_trailer = PdfReader(wmarkfn)
    trailer = PdfReader(inpfn)

    # Handle different sized pages in same document with
    # a memoization cache, so we don't create more watermark
    # objects than we need to (typically only one per document).

    wmark_page = wmark_trailer.pages[0]
    wmark_cache = {}

    # Process every page
    for pagenum, page in enumerate(trailer.pages, 1):

        # Get the media box of the page, and see
        # if we have a matching watermark in the cache
        mbox = tuple(float(x) for x in page.MediaBox)
        odd = pagenum & 1
        key = mbox, odd
        wmark = wmark_cache.get(key)
        if wmark is None:

            # Create and cache a new watermark object.
            wmark = wmark_cache[key] = PageMerge().add(wmark_page)[0]

            # The math is more complete than it probably needs to be,
            # because the origin of all pages is almost always (0, 0).
            # Nonetheless, we illustrate all the values and their names.

            page_x, page_y, page_x1, page_y1 = mbox
            page_w = page_x1 - page_x
            page_h = page_y1 - page_y  # For illustration, not used

            # Scale the watermark if it is too wide for the page
            # (Could do the same for height instead if needed)
            if wmark.w > page_w:
                wmark.scale(1.0 * page_w / wmark.w)

            # Always put watermark at the top of the page
            # (but see horizontal positioning for other ideas)
            wmark.y += page_y1 - wmark.h

            # For odd pages, put it at the left of the page,
            # and for even pages, put it on the right of the page.
            if odd:
                wmark.x = page_x
            else:
                wmark.x += page_x1 - wmark.w

            # Optimize the case where the watermark is same width
            # as page.
            if page_w == wmark.w:
                wmark_cache[mbox, not odd] = wmark

        # Add the watermark to the page
        PageMerge(page).add(wmark, prepend=underneath).render()

    # Write out the destination file
    PdfWriter(outfn, trailer=trailer).write()

def compress_pdf(file_name) :
    ilovepdf = ILovePdf(
        public_key='project_public_a2fc3401f736829aeddc21b9e9f5fc19_7r9JQf696b496cfdaeb3cef6106e8637c8a56', verify_ssl=True)

    task = ilovepdf.new_task('compress')
    task.add_file(file_name)
    task.debug = False
    task.compression_level = 'recommended'
    task.set_output_folder('Pdf')

    task.execute()
    task.download()
    task.delete_current_task()

    os.chdir('./Pdf')
    for file in os.listdir():
        os.rename(file, 'Compressed_Main.pdf')
        break
    os.chdir('../')
