from project import PROJECT_NAME

def project_info(request):
    return {
        'project':{
            'name': PROJECT_NAME,
            'new_msg':'5'}    
    }