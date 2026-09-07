from pathlib import Path
import random,math
root=Path(__file__).resolve().parents[1]
r=random.Random(57)
s=['''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 900"><defs>
<radialGradient id="bowl"><stop stop-color="#30231c"/><stop offset=".68" stop-color="#0b0b0a"/><stop offset=".93" stop-color="#252320"/><stop offset="1" stop-color="#111211"/></radialGradient>
<radialGradient id="heat"><stop stop-color="#f1a45c" stop-opacity=".5"/><stop offset=".5" stop-color="#cf4e1b" stop-opacity=".3"/><stop offset="1" stop-color="#ac3918" stop-opacity="0"/></radialGradient>
<linearGradient id="metal" x2="1" y2="1"><stop stop-color="#837363"/><stop offset=".22" stop-color="#272b28"/><stop offset=".46" stop-color="#b3a392"/><stop offset=".65" stop-color="#242522"/><stop offset="1" stop-color="#777668"/></linearGradient>
<linearGradient id="meat" x2=".1" y2="1"><stop stop-color="#dfba87"/><stop offset=".16" stop-color="#a16a3b"/><stop offset=".4" stop-color="#cc8b4a"/><stop offset=".68" stop-color="#805033"/><stop offset="1" stop-color="#31261d"/></linearGradient>
<linearGradient id="fat" x2="1" y2="1"><stop stop-color="#efd1a6"/><stop offset=".4" stop-color="#b78556"/><stop offset="1" stop-color="#50331e"/></linearGradient>
<filter id="glow"><feGaussianBlur stdDeviation="18"/></filter><filter id="blur"><feGaussianBlur stdDeviation="5"/></filter>
<filter id="texture"><feTurbulence type="fractalNoise" baseFrequency=".31" numOctaves="3" seed="3" result="n"/><feColorMatrix in="n" type="saturate" values="0" result="gray"/><feComponentTransfer in="gray" result="grain"><feFuncA type="linear" slope=".28"/></feComponentTransfer><feComposite in="grain" in2="SourceGraphic" operator="in" result="masked"/><feBlend in="SourceGraphic" in2="masked" mode="soft-light"/></filter>
<clipPath id="clip"><circle cx="450" cy="448" r="320"/></clipPath></defs>
<circle cx="450" cy="490" r="345" fill="#b34d23" opacity=".15" filter="url(#glow)"/>
<circle cx="450" cy="448" r="337" fill="url(#bowl)" stroke="#4e483c" stroke-width="2"/>
<circle cx="450" cy="448" r="326" fill="#111210" stroke="#696254" stroke-width="1"/>
<circle cx="450" cy="455" r="308" fill="url(#heat)"/>
<g clip-path="url(#clip)">''']
for _ in range(170):
    x=r.uniform(140,760);y=r.uniform(140,760)
    if (x-450)**2+(y-448)**2>303**2:continue
    rr=r.uniform(9,29);points=[]
    for j in range(6):
        theta=j*math.pi/3;rd=rr*r.uniform(.7,1.3);points.append(f'{x+rd*math.cos(theta):.1f},{y+rd*math.sin(theta):.1f}')
    color=r.choice(['#252723','#38342b','#494333','#20211e','#292a23','#302a24'])
    glow=r.choice(['#ab4a1c','#7e3c1f','#b45d27','#554831'])
    s.append(f'<polygon points="{" ".join(points)}" fill="{color}" stroke="{glow}" stroke-width="{r.uniform(.5,2):.1f}"/>')
for y in range(137,783,29):
    s.append(f'<path d="M130 {y}H780" stroke="#080909" stroke-width="10"/><path d="M130 {y-1}H780" stroke="#797260" stroke-opacity=".37" stroke-width="2"/>')
s.append('</g><g transform="rotate(-29 450 448)">')
for i,y in enumerate([318,409,501,592]):
    s.append(f'<path d="M104 {y}H793" stroke="#302d26" stroke-width="9"/><path d="M104 {y-1}H793" stroke="url(#metal)" stroke-width="4"/>')
    for j in range(5):
        x=243+j*86+r.uniform(-7,7);yy=y+r.uniform(-5,5)
        w=r.uniform(61,79);h=r.uniform(50,67)
        path=f'M{x-w/2:.1f} {yy-h/2+10:.1f} Q{x-w/2-4:.1f} {yy-h/2-8:.1f} {x-8:.1f} {yy-h/2:.1f} Q{x+20:.1f} {yy-h/2-8:.1f} {x+w/2:.1f} {yy-h/2+8:.1f} L{x+w/2+1:.1f} {yy+20:.1f} Q{x+16:.1f} {yy+h/2+8:.1f} {x-10:.1f} {yy+h/2:.1f} Q{x-w/2-8:.1f} {yy+h/2:.1f} {x-w/2:.1f} {yy-h/2+10:.1f}Z'
        s.append(f'<path d="{path}" fill="#040605" transform="translate(3,8)" opacity=".7"/><path d="{path}" fill="url(#meat)" stroke="#3b2b19" stroke-width="2" filter="url(#texture)"/>')
        if j%2==0:s.append(f'<path d="M{x-24:.1f} {yy-19:.1f}q18 -8 35 2l3 10q-23 -7 -38 -2Z" fill="url(#fat)" opacity=".8"/>')
        for k in [-15,6,24]:
            s.append(f'<path d="M{x+k-7:.1f} {yy-21:.1f}l11 37" stroke="#24190f" stroke-width="{r.uniform(3,6):.1f}" opacity=".64" stroke-linecap="round"/>')
        for k in range(5):
            sx=x+r.uniform(-25,25);sy=yy+r.uniform(-21,21)
            s.append(f'<ellipse cx="{sx:.1f}" cy="{sy:.1f}" rx="{r.uniform(1,3):.1f}" ry="1" fill="#f4d49d" opacity=".62"/>')
s.append('</g>')
for i in range(120):
    a=i*math.pi/60;rad=364;long=i%10==0;end=rad+ (13 if long else 5)
    s.append(f'<path d="M{450+rad*math.cos(a):.2f} {448+rad*math.sin(a):.2f}L{450+end*math.cos(a):.2f} {448+end*math.sin(a):.2f}" stroke="#a59879" opacity="{.5 if long else .16}"/>')
s.append('<circle cx="450" cy="448" r="391" fill="none" stroke="#ac976e" stroke-opacity=".15" stroke-dasharray="2 12"/>')
for i in range(38):
    x=r.uniform(180,760);y=r.uniform(240,805);rr=r.uniform(.7,2.2)
    s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rr:.1f}" fill="#d8ac68" opacity="{r.uniform(.2,.75):.2f}"/>')
s.append('</svg>')
(root/'assets'/'fire-grill.svg').write_text(''.join(s),encoding='utf-8')
print('Original editorial SVG created')
