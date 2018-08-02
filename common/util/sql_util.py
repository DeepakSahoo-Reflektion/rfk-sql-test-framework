import re
def tables_in_query(sql_str):

    # remove the /* */ comments
    q = re.sub(r"/\*[^*]*\*+(?:[^*/][^*]*\*+)*/", "", sql_str)

    # remove whole line -- and # comments
    lines = [line for line in q.splitlines() if not re.match("^\s*(--|#)", line)]

    # remove trailing -- and # comments
    q = " ".join([re.split("--|#", line)[0] for line in lines])

    # split on blanks, parens and semicolons
    tokens = re.split(r"[\s)(;]+", q)

    # scan the tokens. if we see a FROM or JOIN, we set the get_next
    # flag, and grab the next one (unless it's SELECT).

    result = set()
    get_next = False
    for tok in tokens:
        if get_next:
            if tok.lower() not in ["", "select"]:
                result.add(tok)
            get_next = False
        get_next = tok.lower() in ["from", "join"]

    return result

def return_table_name(org_name):
    count_of_dots = org_name.count('.')
    new_name = org_name
    if count_of_dots == 0:
        new_name = 'test_'+org_name
    elif count_of_dots == 1:
        new_name = org_name.split('.')[0]+'.test_'+org_name.split('.')[1]
    elif count_of_dots == 2:
        new_name = org_name.split('.')[0] +'.'+org_name.split('.')[1]+ '.test_' + org_name.split('.')[2]
    else:
        print('error during table name substitution')
    print(org_name)
    print(new_name)
    return new_name

def create_new_sql(org_sql):
    org_table_names = tables_in_query(org_sql)
    pair = {org_name: return_table_name(org_name) for org_name in org_table_names}
    print(pair)
    new_sql = org_sql

    for k,v in pair.items():
        new_sql = new_sql.replace(k,v)

    ##new_sql = org_sql.replace()
    print(new_sql)
    return new_sql

def enrich_sql(org_sql):
    new_sql =create_new_sql(org_sql)
    QRY_TEMPLATE="""{org_sql} UNION {new_sql} MINUS {org_sql} INTERSECT {new_sql}""".format(org_sql=org_sql,new_sql=new_sql)
    print(QRY_TEMPLATE)
    return QRY_TEMPLATE


# SELECT * FROM TEST.EM.be_workflow_step1_inventory_trigger_rows
# UNION
# SELECT * FROM TEST.EM.test_be_workflow_step1_inventory_trigger_rows
# MINUS
# SELECT * FROM TEST.EM.be_workflow_step1_inventory_trigger_rows
# INTERSECT
# SELECT * FROM TEST.EM.test_be_workflow_step1_inventory_trigger_rows;