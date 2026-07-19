#!/usr/bin/env python3


class IncrementalEngine:



    def should_run(self,ctx,step):


        cache=getattr(
            ctx,
            "cache",
            {}
        )


        completed=cache.get(
            "steps",
            []
        )


        if step in completed:


            ctx.log(
                "[=] Skip cached: "
                +
                step
            )


            return False



        return True




    def mark(self,ctx,step):


        if "steps" not in ctx.cache:


            ctx.cache["steps"]=[]



        if step not in ctx.cache["steps"]:


            ctx.cache["steps"].append(
                step
            )



        return ctx

