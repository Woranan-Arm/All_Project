import { LuShirt } from "react-icons/lu";
import { TbTruckDelivery } from "react-icons/tb";
import { TbRosetteDiscount } from "react-icons/tb";
import { CiBadgeDollar } from "react-icons/ci";
import { Link } from "react-router-dom";
import { FaFacebookF } from "react-icons/fa";
import { FaTwitter } from "react-icons/fa";
import { FaInstagram } from "react-icons/fa";
const Footer = () =>{
    return(
        <footer>
            <div className="container">
                <div className="topInfo row">
                    <div className="col d-flex align-items-center">
                        <span><LuShirt/></span>
                        <span className="ml-2">Everyday fresh product</span>
                    </div>

                    <div className="col d-flex align-items-center">
                        <span><TbTruckDelivery /></span>
                        <span className="ml-2">Free dilivery for order</span>
                    </div>

                    <div className="col d-flex align-items-center">
                        <span><TbRosetteDiscount/></span>
                        <span className="ml-2">Daily Mega Discount</span>
                    </div>

                    <div className="col d-flex align-items-center">
                        <span><CiBadgeDollar/></span>
                        <span className="ml-2">Best Price on market</span>
                    </div>
                </div>

            <div className="row mt-5 linksWrap">
                <div className="col">
                    <h5>FRUIT & VEGAN</h5>
                    <ul>
                        <li><Link to="#">Fresh Vegetables</Link></li>
                        <li><Link to="#">Herbs & Seasonings</Link></li>
                        <li><Link to="#">Fresh Fruit</Link></li>
                        <li><Link to="#">Cuts & Sprouts</Link></li>
                        <li><Link to="#">Exotic Fruits & Veggies</Link></li>
                        <li><Link to="#">Packaged Produce</Link></li>
                        <li><Link to="#">Praty Trays</Link></li>
                        
                        
                         
                    </ul>
                </div>

                <div className="col">
                    <h5>BREAKFAST&DAIRY</h5>
                    <ul>
                        <li><Link to="#">Fresh Vegetables</Link></li>
                        <li><Link to="#">Herbs & Seasonings</Link></li>
                        <li><Link to="#">Fresh Fruit</Link></li>
                        <li><Link to="#">Cuts & Sprouts</Link></li>
                        <li><Link to="#">Exotic Fruits & Veggies</Link></li>
                        <li><Link to="#">Packaged Produce</Link></li>
                        <li><Link to="#">Praty Trays</Link></li>
                        
                        
                         
                    </ul>
                </div>

                <div className="col">
                    <h5>FRUIT & SEAFOOD</h5>
                    <ul>
                        <li><Link to="#">Fresh Vegetables</Link></li>
                        <li><Link to="#">Herbs & Seasonings</Link></li>
                        <li><Link to="#">Fresh Fruit</Link></li>
                        <li><Link to="#">Cuts & Sprouts</Link></li>
                        <li><Link to="#">Exotic Fruits & Veggies</Link></li>
                        <li><Link to="#">Packaged Produce</Link></li>
                        <li><Link to="#">Praty Trays</Link></li>
                        
                        
                         
                    </ul>
                </div>

                <div className="col">
                    <h5>BEVERAGES</h5>
                    <ul>
                        <li><Link to="#">Fresh Vegetables</Link></li>
                        <li><Link to="#">Herbs & Seasonings</Link></li>
                        <li><Link to="#">Fresh Fruit</Link></li>
                        <li><Link to="#">Cuts & Sprouts</Link></li>
                        <li><Link to="#">Exotic Fruits & Veggies</Link></li>
                        <li><Link to="#">Packaged Produce</Link></li>
                        <li><Link to="#">Praty Trays</Link></li>
                        
                        
                         
                    </ul>
                </div>

                <div className="col">
                    <h5>BREAD & BEKARY</h5>
                    <ul>
                        <li><Link to="#">Fresh Vegetables</Link></li>
                        <li><Link to="#">Herbs & Seasonings</Link></li>
                        <li><Link to="#">Fresh Fruit</Link></li>
                        <li><Link to="#">Cuts & Sprouts</Link></li>
                        <li><Link to="#">Exotic Fruits & Veggies</Link></li>
                        <li><Link to="#">Packaged Produce</Link></li>
                        <li><Link to="#">Praty Trays</Link></li>
                        
                        
                         
                    </ul>
                </div>
            </div>

            <div className="copyright mt-3 pt-3 pb-3 d-flex">
                <p className="mb-0">Copyright 2024 All right reserved</p>
                    <li className="list-inline-item ml-auto mb-0">
                        <Link to="#"><FaFacebookF/></Link>
                    </li>

                    <li className="list-inline-item">
                        <Link to="#"><FaTwitter/></Link>
                    </li>

                    <li className="list-inline-item">
                        <Link to="#"><FaInstagram/></Link>
                    </li>
            </div>


            </div>
        </footer>
    )
}


export default Footer;