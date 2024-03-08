import sys
import fitz


def img2pdf(img_path):
    # 截取文件名称
    img_name = img_path.split('.')[0]
    doc = fitz.open()

    # 使用fitz打开图片
    imgdoc = fitz.open(img_path)

    # 执行转为pdf方法
    pdfbytes = imgdoc.convert_to_pdf()
    imgpdf = fitz.open("pdf", pdfbytes)

    # 图片插入PDF
    doc.insert_pdf(imgpdf)

    # 保存pdf文件
    doc.save(img_name + '.pdf')
    doc.close()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python script.py <img_path>")
        sys.exit(1)

    img_path = sys.argv[1]

    img2pdf(img_path=img_path)