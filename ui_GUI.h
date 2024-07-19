/********************************************************************************
** Form generated from reading UI file 'GUIsSvwQd.ui'
**
** Created by: Qt User Interface Compiler version 5.15.2
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef GUISSVWQD_H
#define GUISSVWQD_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QComboBox>
#include <QtWidgets/QDialog>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QTextEdit>

QT_BEGIN_NAMESPACE

class Ui_Dialog
{
public:
    QComboBox *comboBox;
    QLineEdit *lineEdit;
    QLabel *label;
    QPushButton *pushButton;
    QPushButton *pushButton_2;
    QLabel *label_2;
    QPushButton *pushButton_3;
    QLabel *label_3;
    QLabel *label_4;
    QTextEdit *textEdit;
    QLabel *label_5;
    QPushButton *pushButton_4;

    void setupUi(QDialog *Dialog)
    {
        if (Dialog->objectName().isEmpty())
            Dialog->setObjectName(QString::fromUtf8("Dialog"));
        Dialog->resize(400, 300);
        comboBox = new QComboBox(Dialog);
        comboBox->addItem(QString());
        comboBox->addItem(QString());
        comboBox->addItem(QString());
        comboBox->addItem(QString());
        comboBox->addItem(QString());
        comboBox->setObjectName(QString::fromUtf8("comboBox"));
        comboBox->setGeometry(QRect(10, 20, 101, 21));
        lineEdit = new QLineEdit(Dialog);
        lineEdit->setObjectName(QString::fromUtf8("lineEdit"));
        lineEdit->setGeometry(QRect(170, 20, 141, 20));
        label = new QLabel(Dialog);
        label->setObjectName(QString::fromUtf8("label"));
        label->setGeometry(QRect(130, 20, 41, 21));
        pushButton = new QPushButton(Dialog);
        pushButton->setObjectName(QString::fromUtf8("pushButton"));
        pushButton->setGeometry(QRect(10, 60, 101, 23));
        pushButton_2 = new QPushButton(Dialog);
        pushButton_2->setObjectName(QString::fromUtf8("pushButton_2"));
        pushButton_2->setGeometry(QRect(10, 100, 61, 21));
        label_2 = new QLabel(Dialog);
        label_2->setObjectName(QString::fromUtf8("label_2"));
        label_2->setGeometry(QRect(130, 60, 261, 21));
        pushButton_3 = new QPushButton(Dialog);
        pushButton_3->setObjectName(QString::fromUtf8("pushButton_3"));
        pushButton_3->setGeometry(QRect(10, 140, 151, 31));
        label_3 = new QLabel(Dialog);
        label_3->setObjectName(QString::fromUtf8("label_3"));
        label_3->setGeometry(QRect(80, 100, 311, 21));
        label_4 = new QLabel(Dialog);
        label_4->setObjectName(QString::fromUtf8("label_4"));
        label_4->setGeometry(QRect(20, 180, 161, 21));
        textEdit = new QTextEdit(Dialog);
        textEdit->setObjectName(QString::fromUtf8("textEdit"));
        textEdit->setGeometry(QRect(190, 170, 201, 121));
        label_5 = new QLabel(Dialog);
        label_5->setObjectName(QString::fromUtf8("label_5"));
        label_5->setGeometry(QRect(250, 140, 91, 21));
        pushButton_4 = new QPushButton(Dialog);
        pushButton_4->setObjectName(QString::fromUtf8("pushButton_4"));
        pushButton_4->setGeometry(QRect(330, 20, 61, 21));

        retranslateUi(Dialog);

        QMetaObject::connectSlotsByName(Dialog);
    } // setupUi

    void retranslateUi(QDialog *Dialog)
    {
        Dialog->setWindowTitle(QCoreApplication::translate("Dialog", "Dialog", nullptr));
        comboBox->setItemText(0, QCoreApplication::translate("Dialog", "Operador/a", nullptr));
        comboBox->setItemText(1, QCoreApplication::translate("Dialog", "J.Armesto", nullptr));
        comboBox->setItemText(2, QCoreApplication::translate("Dialog", "C.Lourenzo", nullptr));
        comboBox->setItemText(3, QCoreApplication::translate("Dialog", "P.Thompson", nullptr));
        comboBox->setItemText(4, QCoreApplication::translate("Dialog", "V.Rostan", nullptr));

        label->setText(QCoreApplication::translate("Dialog", "LUGAR", nullptr));
        pushButton->setText(QCoreApplication::translate("Dialog", "Cargar archivos", nullptr));
        pushButton_2->setText(QCoreApplication::translate("Dialog", "Ruta .csv", nullptr));
        label_2->setText(QCoreApplication::translate("Dialog", "No se observan errores", nullptr));
        pushButton_3->setText(QCoreApplication::translate("Dialog", "Analizar y extraer medidas", nullptr));
        label_3->setText(QCoreApplication::translate("Dialog", "default: Escritorio", nullptr));
        label_4->setText(QCoreApplication::translate("Dialog", "ERRORES: 0", nullptr));
        label_5->setText(QCoreApplication::translate("Dialog", "OBSERVACIONES", nullptr));
        pushButton_4->setText(QCoreApplication::translate("Dialog", "INFO", nullptr));
    } // retranslateUi

};

namespace Ui {
    class Dialog: public Ui_Dialog {};
} // namespace Ui

QT_END_NAMESPACE

#endif // GUISSVWQD_H
