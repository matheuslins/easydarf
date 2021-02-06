

def format_cpf(cpf_raw):
    if len(cpf_raw) < 11:
        cpf_raw = cpf_raw.zfill(11)
    cpf = '{}.{}.{}-{}'.format(
        cpf_raw[:3], cpf_raw[3:6], cpf_raw[6:9], cpf_raw[9:]
    )
    return cpf
