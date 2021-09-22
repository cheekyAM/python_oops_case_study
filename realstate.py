# Real Estate App
# properties=houses,apartments
# list all available properyies
# mark property sold or rented
# agent interface to enter details about roperty


class property:
    def __init__(self,bed='',bath='',ar='',**kwargs):
        super().__init__(**kwargs)
        self.bedrooms=bed
        self.bathrooms=bath
        self.area=ar

    def display(self):
        print("PROPERTY DETAILS")
        print("=======================")
        print("Sqaure footage={2} bedrooms={0} bathrooms={1}".format(self.bedrooms,self.bathrooms,self.area))
        print()

    def prompt_init():
        return dict(ar=input("enter the area: "),
                    bed=input("enter the num of bedrooms "),
                    bath=input("enter the num of bathrooms: "))
    prompt_init=staticmethod(prompt_init)



def get_valid_input(input_string,valid_options):
    input_string +=" ({}) ".format(", ".join(valid_options))
    response=input(input_string)
    while response.lower() not in valid_options:
        response=input(input_string)
    return response



class house(property):
    valid_fenced=('yes','no')
    valid_garage=('attached','detached','none')

    def __init__(self,floors='',garage='',fenced='',**kwargs):
        super().__init__(**kwargs)
        self.floors=floors
        self.garage=garage
        self.fenced=fenced

    def display(self):
        super().display()
        print("HOUSE DETAILS")
        print("# of stories: {}".format(self.floors))
        print("garage: {}".format(self.garage))
        print("fenced yard: {}".format(self.fenced))

    def prompt_init():
        parent_init=property.prompt_init()
        fenced=get_valid_input('is yard fenced? ',house.valid_fenced)
        garage=get_valid_input('is there a garage? ',house.valid_garage)
        floors=input('how many floors? ')
        parent_init.update({
                            "fenced":fenced,
                            "garage":garage,
                            "floors":floors
                        })
        return parent_init
    
    prompt_init=staticmethod(prompt_init)




class apartment(property):
    valid_laundries=("coin","ensuite","none")
    valid_balconies=("yes","no","solarium")

    def __init__(self, balcony='',laundry='',**kwargs) -> None:
        super().__init__(**kwargs)
        self.balcony=balcony
        self.laundry=laundry

    def display(self):
        super().display()
        print(" APARTMENT DETAILS ")
        print("laundry %s" %self.laundry)
        print('has balcony %s' %self.balcony)

    def prompt_init():
        parent_init=property.prompt_init()
        laundry=get_valid_input('what laundry facilities does the property has? ',apartment.valid_laundries)
        balcony=get_valid_input('Does the proprty has a balcony?  ',apartment.valid_balconies)
        parent_init.update({"laundry":laundry,
                            "balcony":balcony})
        return parent_init
    prompt_init=staticmethod(prompt_init)




class purchase:
    def __init__(self, price='',taxes='',**kwargs) -> None:
        super().__init__(**kwargs)
        self.price=price
        self.taxes=taxes

    def display(self):
        super().display()
        print("PURCHASE DETAILS")
        print("selling price: {}".format(self.price))
        print("estimated taxes: {}".format(self.taxes))

    def prompt_init():
        return dict(
                    price=input("what is the selling price? "),
                    taxes=input("what are the estimated taxes? ")
        )
    prompt_init=staticmethod(prompt_init)



class rental:
    def __init__(self,furnished='',utilities='',rent='',**kwargs):
        super().__init__(**kwargs)
        self.furnished=furnished
        self.utilities=utilities
        self.rent=rent

    def display(self):
        super().display()
        print("RENTAL DETAILS")
        print("rent: {}".format(self.rent))
        print("estimated utilities: {}".format(self.utilities))
        print("furnished: {}".format(self.furnished))

    def prompt_init():
        return dict(
                    rent=input("What is the monthly rent? "),
                    utilities=input("What are the estimated utilities? "),
                    furnished = get_valid_input("Is the property furnished? ",("yes", "no")))
    prompt_init = staticmethod(prompt_init)



class houserental(rental,house):
    def prompt_init():
        init=house.prompt_init()
        init.update(rental.prompt_init())
        return init
    
    prompt_init=staticmethod(prompt_init)


class apartmentrental(rental,apartment):
    def prompt_init():
        init=apartment.prompt_init()
        init.update(rental.prompt_init())
        return init
    prompt_init=staticmethod(prompt_init)


class apartmentpurchase(purchase,apartment):
    def prompt_init():
        init=apartment.prompt_init()
        init.update(purchase.prompt_init())
        return init
    prompt_init=staticmethod(prompt_init)


class housepurchase(purchase,house):
    def prompt_init():
        init=house.prompt_init()
        init.update(purchase.prompt_init())
        return init
    prompt_init=staticmethod(prompt_init)
    
    

class Agent:
    def __init__(self) -> None:
        self.property_list=[]

    def display_properties(self):
        for prop in self.property_list:
            prop.display()

    type_map={
                ('house','rental'):houserental,
                ('house','purchase'):housepurchase,
                ('apartment','purchase'):apartmentpurchase,
                ('apartment','rental'):apartmentrental
    }
    
    def add_property(self):
        property_type=get_valid_input('what type of property? ',('house','apartment')).lower()
        payment_type=get_valid_input('what payment type',('purchase','rental')).lower()
        propertyclass=self.type_map[(property_type,payment_type)]
        init_args=propertyclass.prompt_init()
        print(init_args)
        self.property_list.append(propertyclass(**init_args))