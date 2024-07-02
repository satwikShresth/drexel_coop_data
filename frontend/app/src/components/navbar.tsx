import React from 'react';
import { Link, useMatch, useResolvedPath } from 'react-router-dom';

interface LinkProps { to: string; label: string; }
interface NavBarProps { links: LinkProps[]; }
const NavBar: React.FC<NavBarProps> = ({ links }) => {
   return (
      <nav className="bg-gray-800 p-4 fixed top-0 left-0 w-full z-10">
         <div className="container mx-auto flex justify-between items-center">
            <Link to="/" className="text-white text-lg font-semibold">
               DACD
            </Link>
            <ul className="space-x-4 flex">
               {links.map(link => (
                  <CustomLink key={link.to} to={link.to}>
                     {link.label}
                  </CustomLink>
               ))}
            </ul>
         </div>
      </nav>
   );
};

interface CustomLinkProps { to: string; children: React.ReactNode; }
const CustomLink: React.FC<CustomLinkProps> = ({ to, children, ...props }) => {
   const resolvedPath = useResolvedPath(to);
   const isActive = useMatch({ path: resolvedPath.pathname, end: true });

   return (
      <li className={isActive ? "text-white" : "text-gray-300 hover:text-white"}>
         <Link to={to} {...props}>
            {children}
         </Link>
      </li>
   );
};

export default NavBar;
