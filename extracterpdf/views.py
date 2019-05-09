from django.shortcuts import render
from .forms import Destinosform
from .models import Destinos
from uploader.models import Culturatemp
from django.shortcuts import HttpResponse
import PyPDF2
import os
import re
from datetime import datetime
from website.settings import BASE_DIR


def index(request):

    if not request.user.is_authenticated:
        return render(request, 'biao/hrdb_visitor.html')

    uploader = request.user.groups.filter(name='Uploaders').exists()
    if not uploader:
            return render(request, 'biao/hrdb.html', {'uploader': False})

    if request.method != 'POST':
        form = Destinosform()
        return render(request, "extracterpdf/index.html", {'uploader': True, 'form': form})

    file_form = Destinosform(request.POST, request.FILES)
    files = request.FILES.getlist('pdffile')
    if file_form.is_valid():
        for f in files:
            file_instance = Destinos(pdffile=f)
            file_instance.save()

        todas_culturas = []
        pre_path_pdfs = os.path.join(BASE_DIR, "static", "extracterpdf")
        path_pdfs = os.path.join(pre_path_pdfs, "pdfs_extraidos")
        #path_pdfs = r"extracterpdf\static\pdfs_extraidos"
        for filename in os.listdir(path_pdfs):
            culturas = []
            falha = None
            nome = 'ignorado'
            texto_extraido = texto_extraido_de_culturas_em_pdf(filename, path_pdfs)
            texto_extraido = realiza_subs(texto_extraido)
            nome, protocolo, medico, data, unidade, coleta = cabecalho(texto_extraido)
            miolo_processado = processa_miolo(texto_extraido)
            amostras_analisadas = analisa_amostras(miolo_processado)
            antibiogramas = extrai_antibiogramas(texto_extraido)
            if coleta is not None:
                coleta = datetime.strptime(coleta,'%d/%m/%Y')
            if data is not None:
                data = datetime.strptime(data,'%d/%m/%Y')

            for amostra_analisada in amostras_analisadas:
                material = amostra_analisada[0]
                resultado = amostra_analisada[1]
                tipo = amostra_analisada[2]
                if resultado == 'negativa':
                    tipo = None
                testes = amostra_analisada[3]
                mat_especifico = amostra_analisada[4]
                culturas.append({'filename': filename,
                                 'nome': nome,
                                 'prot': protocolo,
                                 'medico': medico,
                                 'data': data,
                                 'unid': unidade,
                                 'coleta': coleta,
                                 'material': material,
                                 'mat_especifico': mat_especifico,
                                 'resultado': resultado,
                                 'tipo': tipo,
                                 'testes': testes,
                                 'falha': falha,
                                 'ami': None,
                                 'amp': None,
                                 'asb': None,
                                 'atm': None,
                                 'caz': None,
                                 'cip': None,
                                 'cli': None,
                                 'cpm': None,
                                 'cro': None,
                                 'ctn': None,
                                 'eri': None,
                                 'ert': None,
                                 'gen': None,
                                 'imi': None,
                                 'lin': None,
                                 'mer': None,
                                 'nit': None,
                                 'nor': None,
                                 'oxa': None,
                                 'pen': None,
                                 'pol': None,
                                 'ppt': None,
                                 'str': None,
                                 'sut': None,
                                 'tei': None,
                                 'tet': None,
                                 'van': None})

            for cultura in culturas:
                for antibiograma in antibiogramas:
                    if cultura['tipo'] == antibiograma['tipo']:
                        resultadosComTipo = [(cultura['resultado'], cultura['tipo']) for cultura in culturas if cultura['tipo'] == antibiograma['tipo']]
                        countResutladosUnicosComTipo = len(set(resultadosComTipo))
                        if countResutladosUnicosComTipo > 1:
                            cultura['falha'] = 'sim'
                        else:
                            cultura.update(antibiograma)
                            break

            for cultura in culturas:
                todas_culturas.append(cultura)
                cultura_temp = Culturatemp(**cultura)
                cultura_temp.save()


        return render(request, "extracterpdf/extraido.html", {'uploader': True, 'todas_culturas': todas_culturas})
    return HttpResponse('<h1>form is not valid</h1>')


def realiza_subs(t):
    t = t.lower()
    t = re.sub(r'mente resistente a.+', '', t)
    t = re.sub(r'Oxacilina prediz resistência a outros beta-lactâmicos \(Cefalosporinas, carbapenens, entre outros\)', '', t)
    t = re.sub(r'\bMIC para \w+', '', t)
    t = re.sub(r'Aztreonam e Penicilinas', '', t)
    t = re.sub(r'Clindamicina (positivo|negativo)', '', t)
    t = re.sub(r'Sulf./', '', t)
    t = re.sub(r'única de hemocultura', '', t)
    t = re.sub(r'hemocultura, devido', '', t)
    t = re.sub(r'Antibiograma da urocultura', '', t)
    return t


def extrai_antibiogramas(texto_extraido):
    atb_patts = {'pol': 'polimixina?', 'nor': 'norfloxacin[ao]?', 'asb (1)': 'amp\. sulbactam',
                 'asb (2)': 'ampicilina/sulbactam', 'nit': 'nitrofurantoina?', 'str': 'estreptomicina',
                 'str(HLAR)': 'estreptomicina ?\(HR?LA?R?\)', 'sut (1)': 'trimetropima?',
                 'sut (2)': 'trimetoprim-Sulf\.?',
                 'pen': 'penicilina', 'eri': 'eritromicina', 'amp': 'ampicilina', 'cli': 'clindamicina',
                 'lin': 'linezolid[ae]', 'tet': 'tetraciclina', 'van': 'vancomicina', 'tei': 'teicoplanina',
                 'ctn': 'cefalotina', 'oxa': 'oxacilina', 'ami': 'amicacina', 'gen': 'gentamicina',
                 'gen(HLAR)': 'gentamicina ?\(HR?LA?R?\)', 'caz': 'ceftazidima', 'cro': 'ceftriaxon[ae]',
                 'cpm': 'cefepime',
                 'cip': 'ciprofloxacin[oa]?', 'imi': 'imip[ei]nem', 'mer': 'meropenem', 'ert': 'ertapenem',
                 'ppt (1)': 'piperacic?lina[- ]ta[zx]obactam', 'ppt (2)': 'pip\.?[- ]ta[zx]obactam', 'atm': 'aztreonam'}
    test_list = []
    atbg = []
    for k, atb_patt in atb_patts.items():
        pt = re.compile(r'(' + atb_patt + '):?(sens[íi]vel|resistente|intermedi[aá]rio)', re.I)
        i = re.finditer(pt, texto_extraido)
        for m in i:
            atbg.append((m.start(1), k[:3], m.group(2)))
            test_list.append((m.start(1), m.end(1)))
    test_list.sort()
    if len(test_list) > 0:
        start_index_antibiograma_2 = test_list[-1][1]
        for j in range(1, len(test_list) - 1):
            if test_list[j][0] - test_list[j - 1][1] > 17:
                start_index_antibiograma_2 = test_list[j][0]

    antibiograma1 = {}
    antibiograma2 = {}
    for item in atbg:
        if item[0] < start_index_antibiograma_2:
            antibiograma1[item[1]] = item[2][:1]
        if item[0] >= start_index_antibiograma_2:
            antibiograma2[item[1]] = item[2][:1]

    antibiogramas = [antibiograma1, antibiograma2]
    for atbgr in antibiogramas:
        if 'str' in atbgr.keys():
            atbgr['tipo'] = 'enterococcus'
        elif 'cro' in atbgr.keys() and 'mer' in atbgr.keys() and 'ppt' in atbgr.keys():
            atbgr['tipo'] = 'bgnf'
        elif 'oxa' in atbgr.keys() or 'lin' in atbgr.keys():
            atbgr['tipo'] = 'staph'
        elif 'caz' in atbgr.keys() and 'caz' in atbgr.keys() and ('cro') not in atbgr.keys():
            atbgr['tipo'] = 'bgnnf'
        else:
            atbgr['tipo'] = 'desconhecido'
    return antibiogramas


def texto_extraido_de_culturas_em_pdf(filename, path_pdfs):
    texto_extraido = None
    if filename.endswith(".pdf"):
        leitor = PyPDF2.PdfFileReader(path_pdfs + '//' + filename)
        texto_extraido = leitor.getPage(0).extractText()
    return texto_extraido


def processa_miolo(texto_a_ser_processado):
    amostra_marks = ["Hemocultura", "Urocultura", "Cultura de Materiais", "cultura da agua"]
    miolo = texto_a_ser_processado.lower()
    for mark in amostra_marks:
        miolo = miolo.replace(mark.lower(), "&" + mark.lower())
    materiais = miolo.split("&")
    return materiais[1:]


def analisa_amostras(lista_de_culturas1):
    global c_material
    # A funcao recebe uma lista de strings, sendo cada string uma amostra, ainda sem analise
    # A funcao analisa cada string da lista enviada, utilizando os criterios elencados no dicionario abaixo "chaves"
    # A funcao retorna uma lista de tuplas-5 (mat, agente, tipo, testes, mat_esp), sendo cada tupla-3 referente a uma amostra
    # Pendente ainda fazer o antibiograma
    chaves = {
        "não foram isolados": "negativa",
        "ausência de crescimento bacteriano": "negativa",
        "acinetobacter baumanii": "acinetobacter baumanii",
        "pseudomonas aeruginosa": "pseudomonas aeruginosa",
        "staphylococcus coagulase negativo": "staphylococcus coagulase negativo",
        "klebsiella pneumoniae": "klebsiella sp",
        "klebsiella Pneumoniae": "klebsiella sp",
        "enterococcus sp": "enterococcus sp",
        "microbiota mista": "microbiota mista",
        "citrobacter freundii": "citrobacter sp",
        "cândida não albicans": "cândida não albicans",
        "serratia liquefaciens": "serratia sp",
        "staphylococcus aureus": "staphylococcus aureus",
        "citrobacter diversus": "citrobacter sp",
        "escherichia coli": "escherichia coli",
        "serratia sp": "serratia sp",
        "cândida albicans": "cândida albicans",
        "serratia marcescens": "serratia sp",
        "pseudomonas sp": "pseudomonas aeruginosa",
        "candida spp": "candida spp",
        "proteus penneri": "proteus sp",
        "klebsiella sp": "klebsiella sp",
        "crescimento da microbiota normal": "microbiota normal",
        "cândida sp": "cândida sp",
        "streptococcus pneumoniae": "streptococcus pneumoniae",
        "enterococcus faecalis": "enterococcus sp",
        "streptococcus sp": "streptococcus sp",
        "ausência de coliformes": "ausência de coliformes",
        "presença de coliformes": "presença de coliformes",
        "staphyloccoccus aureus": "staphylococcus aureus",
        "smicrorganismonegativanegativa": "negativa",
        "enterobacter aerogenes": "enterobacter sp",
        "morganella morganni": "morganella morganni",
        "morganella morganii": "morganella morganni",
        "crescimento de microbiota normal": "microbiota normal",
        "proteus mirabilis": "proteus sp",
        "hemocultura - aerobios2a amostramétodo:cultura em meio especificoamostra: sangue total" : "negativa"
        }
    materiais_analisados = []
    for material in lista_de_culturas1:
        mat = None
        agente = None
        tipo = None
        testes = None
        mat_esp = None
        # Abaixo, condicional que define o mat (MATERIAL)
        if "hemocultura" in material:
            mat = "hemo"
        elif "urocultura" in material:
            mat = "uro"
        elif "cultura de materiais" in material:
            mat = "cm"
        elif "cultura da agua" in material:
            mat = "agua"
        # Abaixo, loop para definir o RESULTADO (referido como agente), utilizando os valores do dicionario chaves acima
        for chave, valor in chaves.items():
            if chave in material:
                agente = valor
                tipo = 'desconhecido'
                if 'escherichia' in agente or 'serratia' in agente or 'klebsiella' in agente or 'citrobacter' in agente or 'proteus' in agente or 'morganella' in agente or 'enterobacter' in agente:
                    tipo = 'bgnf'
                if 'pseudomonas' in agente or 'acinetobacter' in agente:
                    tipo = 'bgnnf'
                if 'staph' in agente:
                    tipo = 'staph'
                if 'enteroc' in agente:
                    tipo = 'enterococcus'
                if 'ndida' in agente:
                    tipo = 'candida'
                if 'mista' in agente:
                    tipo = None
                break
        if 'esbl' in material:
            testes = 'esbl'
        if 'hodge' in material:
            testes = 'kpc'
        if 'mrsa' in material:
            testes = 'mrsa'
        if 'kpc' in material:
            testes = 'kpc'
        if 'carbapenemase' in material:
            testes = 'kpc'
        if mat == 'cm':
            c_material = re.compile(r'material:? ?(?P<mati>.+?) ?(?=m[ée]todo|data|cerca|coleta|\n)', re.I)
            material_especifico = c_material.search(material)
            if material_especifico != None:
                mat_esp = material_especifico.group('mati')
        materiais_analisados.append((mat, agente, tipo, testes, mat_esp))
    return materiais_analisados


def cabecalho(t):
    c_cabecalho = re.compile(r"(.*?)protocolo:(\d*?)paciente:medico:(.*?)susconvenio:.*(\d\d/\d\d/\d\d\d\d)documento:(\w*?)hospital", re.I)
    cabecalho = c_cabecalho.finditer(t)
    nome = protocolo = medico = data = unidade = None
    for item in cabecalho:
        nome = item.group(1)
        protocolo = item.group(2)
        medico = item.group(3)
        data = item.group(4)
        unidade = item.group(5)

    c_datas = re.compile(r'(?<!/)(\d\d/\d\d)(?!/)', re.I)
    coleta = c_datas.search(t)
    if coleta != None:
        try:
            coleta = coleta.group(0) + "/" + data[-4:]
            # if para corrigir o problema de herdar o ano errado quando coleta dez e data jan
            if data[3:5] == '01' and coleta[3:5] == '12':
                coleta = coleta[:-4] + str(int(data[-4:]) - 1)
        except TypeError:
            coleta = None

    else:
        coleta = None
    return nome, protocolo, medico, data, unidade, coleta
