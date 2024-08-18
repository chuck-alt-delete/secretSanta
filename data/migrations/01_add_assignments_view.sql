create view assignments as
        select 
            u1.name as gifter, 
            u2.name as giftee, 
            year 
        from 
            SecretSantaAssignments s 
            join users u1 on s.gifter_id = u1.id 
            join users u2 on s.giftee_id = u2.id
        order by year desc;