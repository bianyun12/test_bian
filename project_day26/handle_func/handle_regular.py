import re
from handle_func.handle_config import conf
class handle_regular_class:
    def replace_data(item,cls):
        while re.search("#(.+?)#",item):

            data=re.search("#(.+?)#",item)
            # print(data)
            repla_data=data.group()
            # print(repla_data)
            key=data.group(1)
            # print(key)
            try:
                value=conf.get("test_data",key)
                # print(value)
            except:
                value=getattr(cls,key)
                # print(value)
            item=item.replace(repla_data,str(value))
        return item
if __name__=="__main__":
    case = '{"mobile_phone":"#mobile_phone#","pwd":"#pwd#"}'
    item1=handle_regular_class.replace_data(case,handle_regular_class)
    print(item1)

